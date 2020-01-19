import time
from . import bridgeFinder
from . import keySetup
from . import HTTPS

class apiManager():
    ### Static class variables ###
    CONFIG_NAME = "apiMan"
    CONFIG_ADDR = "address"
    CONFIG_KEY = "key"
    KWARG_ADDR = CONFIG_ADDR
    KWARG_KEY = CONFIG_KEY
    KWARG_VERBOSE = "verbose"
    UPDATE_INTERVAL = 1000
    HS_COLORMODE = "hs"
    XY_COLORMODE = "xy"

    def __init__(self, **kwargs):
        self.__lights = None
        self.__lastUpdate = 0
        # Get variables
        self.__api = {apiManager.KWARG_ADDR: kwargs.get(apiManager.KWARG_ADDR, None), apiManager.KWARG_KEY: kwargs.get(apiManager.KWARG_KEY, None)}
        self.__verbose = kwargs.get(apiManager.KWARG_VERBOSE, False)
        if not self.isReady():
            if self.__verbose:
                print("No API address or key given - Run configAPI()")

    def setAPIconfig(address, key):
        if address != None and key != None:
            self.__api = {apiManager.KWARG_ADDR: address, apiManager.KWARG_KEY: key}
            return True
        else:
            return False

    def isReady(self):
        return self.__api[apiManager.KWARG_ADDR] != None and self.__api[apiManager.KWARG_KEY] != None

    def configAPI(self):
        if not self.isReady():
            devices = bridgeFinder.scanNetwork()
            if devices != None:
                if len(devices) > 1:
                    print("More then one bridge found, which was unexpected.")
                else:
                    address = devices[0]
                    key = keySetup.getAPIkey(address)
                    if key == None:
                        print("Could not obtain key from API.")
                        return False
                    self.__api[apiManager.KWARG_ADDR] = address
                    self.__api[apiManager.KWARG_KEY] = key
                    return True
            else:
                print("No bridge found, cannot configure API.")
                return False

    def getAPIconfig(self):
        return self.__api

    def getLights(self, force = False):
        timeNow = time.time()
        if force == True or self.__lights == None or (timeNow - self.__lastUpdate) > apiManager.UPDATE_INTERVAL:
            self.__lights = self.__requestLightsFromBridge()
            self.__lastUpdate = timeNow
            if self.__verbose:
                print("Found {} lights with data {}".format(len(self.__lights), self.__lights))
        return self.__lights

    def __requestLightsFromBridge(self):
        response_code, data = HTTPS.request(HTTPS.GET, self.__api[apiManager.KWARG_ADDR], "/api/" + self.__api[apiManager.KWARG_KEY] + "/lights")
        self.__lightConfig = {}
        lights = []
        lightData = []
        if data != None:
            for light in data:
                lights.append(light)
        if len(lights) > 0:
            for i in range(0, len(lights)):
                try:
                    lightID = lights[i]
                    lightName = data[lightID]["name"]
                    ligthMode = data[lightID]["state"]["colormode"]
                    lightData.append({"id": lightID, "name": lightName, "colormode": ligthMode})
                    self.__lightConfig[lightID] = ligthMode
                except:
                    print("Exception on apiManager() -> __requestLightsFromBridge(): Light data does not contain expected entries")
        return lightData

    def setColor(self, lightID, sR, sG, sB):
        params = self.__determineColormode(lightID, int(sR), int(sG), int(sB))
        if params != None:
            response_code, data = HTTPS.request(HTTPS.PUT, self.__api[apiManager.KWARG_ADDR], "/api/" + self.__api[apiManager.KWARG_KEY] + "/lights/" + lightID + "/state", params = params, dataType = "json", verbose = True)
            print("Bridge responded with {} and data {}".format(response_code, data))
            if response_code < 202:
                return True
        
        return False

    def __determineColormode(self, lightID, R, G, B):
        try:
            colormode = self.__lightConfig[lightID]
        except:
            colormode = apiManager.HS_COLORMODE
            print("Exception on apiManager() -> __determineColormode(): No config found for lightID {}".format(lightID))
        switcher = {
            apiManager.XY_COLORMODE: self.__convertRGBtoXY,
            apiManager.HS_COLORMODE: self.__convertRGBtoHS
        }
        function = switcher.get(colormode, lambda: self.__invalidColormode)
        return function(R, G, B)

    def __invalidColormode(self, R, G, B):
        return self.__convertRGBtoHS(R, G, B)

    def __convertRGBtoXY(self, R, G, B):
        fR, fG, fB = self.__RGBtoFloat(R, G, B)
        # Convert RGB ot XYZ
        tx = fR * 0.649926 + fG * 0.103455 + fB * 0.197109
        ty = fR * 0.234327 + fG * 0.743075 + fB * 0.022598
        tz = fG * 0.053077 + fB * 1.035763
        # Find x and y
        x = tx / (tx + ty + tz)
        y = tx / (tx + ty + tz)
        #### Check if within color gamut capabilities of light - WIP
        bri = 255 * ty
        return self.__getXYparams(x, y, int(bri))

    def __convertRGBtoHS(self, R, G, B):
        # Convert RGB to fraction of RGB from 0 to 1.
        fR, fG, fB = self.__RGBtoFloat(R, G, B)
        # Get maximum value
        Cmax = max(fR, fG, fB)
        # Get minimum value
        Cmin = min(fR, fG, fB)
        # Get difference
        delta = Cmax - Cmin
        # Get hue
        hue = 0
        if delta == 0:
            pass
        elif Cmax == fR:
            hue = (65535/6) * (((fG - fB) / delta) % 6)
        elif Cmax == fG:
            hue = (65535/6) * (((fB - fR) / delta) + 2)
        elif Cmax == fB:
            hue = (65535/6) * (((fR - fG) / delta) + 4)
        # Get brightness
        bri = ((Cmax - Cmin) / 2)
        # Get saturation
        sat = 0
        if delta != 0:
            sat = 255 * (delta / (1 - abs((2 * bri) - 1)))
        # Get brightness (of 0 to 255)
        bri = 255 * bri
        return self.__getHSparams(int(hue), int(sat), int(bri))

    def __RGBtoFloat(self, R, G, B):
        # Convert RGB to float value (ratioes from 0 to 1 - instead of between 0 255)
        return R/255, G/255, B/255

    def __getXYparams(self, x, y, bri):
        return {"bri": bri, "on": True, "xy": [x, y], "transitiontime": 1}

    def __getHSparams(self, hue, sat, bri):
        return {"bri": bri, "hue": hue, "on": True, "sat": sat, "transitiontime": 1}