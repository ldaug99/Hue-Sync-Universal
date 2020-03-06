import time
from rgbxy import Converter
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
    UPDATE_INTERVAL = 100
    #HS_COLORMODE = "hs"
    #XY_COLORMODE = "xy"
    KWARG_BRI = "bri" # Kwarg to force brightness to a certain value

    HUE_C = [
        [0.649926, 0.103455, 0.197109],
        [0.234327, 0.743075, 0.022598],
        [0.000000, 0.053077, 1.035763]
    ]

    GAMUT_C = [
        [0.6068909, 0.1735011, 0.2003480],
        [0.2989164, 0.5865990, 0.1144845],
        [0.0000000, 0.0660957, 1.1162243]
    ]

    CIE_XYZ = [
        [0.49000, 0.31000, 0.20000],
        [0.17697, 0.81240, 0.01063],
        [0.00000, 0.01000, 0.99000]
    ]

    matrix = [
	    [0.4123865632529917,   0.35759149092062537, 0.18045049120356368],
	    [0.21263682167732384,  0.7151829818412507,  0.07218019648142547],
	    [0.019330620152483987, 0.11919716364020845, 0.9503725870054354]
    ]

    REF_WHITE = HUE_C

    def __init__(self, **kwargs):
        self.__lights = None
        self.__lastUpdate = 0
        # Get variables
        self.__api = {apiManager.KWARG_ADDR: kwargs.get(apiManager.KWARG_ADDR, None), apiManager.KWARG_KEY: kwargs.get(apiManager.KWARG_KEY, None)}
        self.__verbose = kwargs.get(apiManager.KWARG_VERBOSE, False)
        self.__froceBri = kwargs.get(apiManager.KWARG_BRI, None)
        self.__converter = Converter()
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
        #self.__lightConfig = {}
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
                    #ligthMode = data[lightID]["state"]["colormode"]
                    lightData.append({"id": lightID, "name": lightName})
                    #lightData.append({"id": lightID, "name": lightName, "colormode": ligthMode})
                    #self.__lightConfig[lightID] = ligthMode
                except:
                    print("Exception on apiManager() -> __requestLightsFromBridge(): Light data does not contain expected entries")
        return lightData

    #def setColor(self, lightID, sR, sG, sB, sbri):
    def setColor(self, lightID, sR, sG, sB):
        # https://medium.com/hipster-color-science/a-beginners-guide-to-colorimetry-401f1830b65a
        #params = self.__determineColormode(lightID, int(sR), int(sG), int(sB))
        #params = self.__convertRGBtoXY(int(sR), int(sG), int(sB), int(sbri))
        #params = self.__convertRGBtoXY(int(sR), int(sG), int(sB))
        params = self.__easyXY(int(sR), int(sG), int(sB))
        if params != None:
            response_code, data = HTTPS.request(HTTPS.PUT, self.__api[apiManager.KWARG_ADDR], "/api/" + self.__api[apiManager.KWARG_KEY] + "/lights/" + lightID + "/state", params = params, dataType = "json", verbose = True)
            print("Bridge responded with {} and data {}".format(response_code, data))
            if response_code < 202:
                return True
        return False

    def __easyXY(self, R, G, B):
        param = self.converter(R, G, B)
        x = param[0]
        y = param[1]
        return self.__getXYparams(x, y, 254)

    # def __determineColormode(self, lightID, R, G, B):
    #     try:
    #         colormode = self.__lightConfig[lightID]
    #     except:
    #         colormode = apiManager.HS_COLORMODE
    #         print("Exception on apiManager() -> __determineColormode(): No config found for lightID {}".format(lightID))
    #     switcher = {
    #         apiManager.XY_COLORMODE: self.__convertRGBtoXY,
    #         apiManager.HS_COLORMODE: self.__convertRGBtoHS
    #     }
    #     function = switcher.get(colormode, lambda: self.__invalidColormode)
    #     return function(R, G, B)

    # def __invalidColormode(self, R, G, B):
    #     return self.__convertRGBtoHS(R, G, B)

    #def __convertRGBtoXY(self, R, G, B, bri):
    def __convertRGBtoXY(self, R, G, B):
        if R != 0 and G != 0 and B != 0:
            fR, fG, fB = self.__RGBtoFloat(R, G, B)
            # Convert RGB ot XYZ
            tx = fR * apiManager.REF_WHITE[0][0] + fG * apiManager.REF_WHITE[0][1] + fB * apiManager.REF_WHITE[0][2]
            ty = fR * apiManager.REF_WHITE[1][0] + fG * apiManager.REF_WHITE[1][1] + fB * apiManager.REF_WHITE[1][2]
            tz = fR * apiManager.REF_WHITE[2][0] + fG * apiManager.REF_WHITE[2][1] + fB * apiManager.REF_WHITE[2][2]
            if self.__verbose:
                print("Calculated x {}, y {} and z {}".format(tx,ty,tz))
            # Find x and y
            x = round(tx / (tx + ty + tz), 2)
            y = round(ty / (tx + ty + tz), 2)
            #### Check if within color gamut capabilities of light - WIP
            #bri = round((254 * ty) + (254 - ty) * (bri / 255))
            if self.__froceBri != None:
                bri = self.__froceBri
            else:
                bri = round(254 * ty)
            if self.__verbose:
                print("RBG to XYZ returnes: xy [{} , {}], brightness {}".format(x,y,bri))
            return self.__getXYparams(x, y, int(bri))
        else:
            if self.__verbose:
                print("Color input zero, setting brightness zero")
            return self.__getXYparams(0.4, 0.4, 0)
    # def __convertRGBtoHS(self, R, G, B):
    #     # Convert RGB to fraction of RGB from 0 to 1.
    #     fR, fG, fB = self.__RGBtoFloat(R, G, B)
    #     # Get maximum value
    #     Cmax = max(fR, fG, fB)
    #     # Get minimum value
    #     Cmin = min(fR, fG, fB)
    #     # Get difference
    #     delta = Cmax - Cmin
    #     # Get hue
    #     hue = 0
    #     if delta == 0:
    #         pass
    #     elif Cmax == fR:
    #         hue = (65535/6) * (((fG - fB) / delta) % 6)
    #     elif Cmax == fG:
    #         hue = (65535/6) * (((fB - fR) / delta) + 2)
    #     elif Cmax == fB:
    #         hue = (65535/6) * (((fR - fG) / delta) + 4)
    #     # Get brightness
    #     bri = ((Cmax - Cmin) / 2)
    #     # Get saturation
    #     sat = 0
    #     if delta != 0:
    #         sat = 255 * (delta / (1 - abs((2 * bri) - 1)))
    #     # Get brightness (of 0 to 255)
    #     bri = 255 * bri
    #     return self.__getHSparams(int(hue), int(sat), int(bri))

    def __RGBtoFloat(self, R, G, B):
        # Convert RGB to float value (ratioes from 0 to 1 - instead of between 0 255)
        return R / 255.0, G / 255.0, B / 255.0

    def __getXYparams(self, x, y, bri):
        return {"on": True, "bri": bri, "xy": [x, y], "transitiontime": 0}

    # def __getHSparams(self, hue, sat, bri):
    #     return {"bri": bri, "hue": hue, "on": True, "sat": sat, "transitiontime": 1}