import time
from . import bridgeFinder
from . import keySetup
from . import HTTPS

class apiManager():
    ### Static class variables ###
    CONFIG_NAME = "apiMan"
    KWARG_ADDR = "address"
    KWARG_KEY = "key"
    KWARG_VERBOSE = "verbose"
    UPDATE_INTERVAL = 1000

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
        lights = []
        lightData = []
        if data != None:
            for light in data:
                lights.append(light)
        if len(lights) > 0:
            for i in range(0, len(lights)):
                lightID = lights[i]
                lightName = data[lightID]["name"]
                lightData.append({"id": lightID, "name": lightName})
        return lightData
        
    def setColor(self, lightID, hue, sat, bri):
        params = {"bri": int(bri), "hue": int(hue), "on": True, "sat": int(sat)}
        response_code, data = HTTPS.request(HTTPS.PUT, self.__api[apiManager.KWARG_ADDR], "/api/" + self.__api[apiManager.KWARG_KEY] + "/lights/" + lightID + "/state", params = params)
        print("Bridge responded with {}".format(response_code))
        if response_code < 202:
            return True
        else:
            return False