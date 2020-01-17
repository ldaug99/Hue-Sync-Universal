from common import HTTPS
import time

class lightManager():
    __address = None
    __key = None
    __verbose = False

    __lights = None
    __lastUpdate = 0
    __updateInterval = 1000

    CENTER = 0
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4

    __groups = ["center", "left", "right", "top", "bottom"]

    __lightGroups = {
        __groups[CENTER]: [],
        __groups[LEFT]: [],
        __groups[RIGHT]: [],
        __groups[TOP]: [],
        __groups[BOTTOM]: []
    }

    def __init__(self, address, key, **kwargs):
        self.__address = address
        self.__key = key
        self.__verbose = kwargs.get('verbose', False)

    def addLight(self, lightID, group = "center"):
        if not self.__getDuplicatesInGroup(lightID, group):
            lights = self.getLights()
            for lid in range(0, self.__getNumOfLights(lights)):
                if str(lights[lid]["id"]) == lightID:
                    self.__lightGroups[group].append(lights[lid])
                    if self.__verbose:
                        print("Added {} to group {}, {}".format(lightID, group, self.__lightGroups))
                    return True
        else:
            if self.__verbose:
                print("Light {} aldready in group {}".format(lightID, group))
        return False

    def __getDuplicatesInGroup(self, lightID, group):
        indexes = []
        for lid in range(0, self.__getNumOfLights(self.__lightGroups[group])):
            if str(self.__lightGroups[group][lid]["id"]) == lightID:
                indexes.append(lid)
        return indexes

    def removeLight(self, lightID):
        pass

    def getLights(self):
        if self.__lights == None or (time.time() - self.__lastUpdate) > self.__updateInterval:
            self.__lights = self.__requestLightsFromBridge()
            if self.__verbose:
                print("Found {} lights with data {}".format(len(self.__lights), self.__lights))
        return self.__lights

    def setColor(self, lightID, hue, sat, bri):
        params = {"bri": int(bri), "hue": int(hue), "on": True, "sat": int(sat)}
        response_code, data = HTTPS.request(HTTPS.PUT, self.__address, "/api/" + self.__key + "/lights/" + lightID + "/state", params = params)
        print("Bridge responded with {}".format(response_code))

    def setGroupColor(self, groupe, RGB):
        pass

    def getGroupSetup(self):
        return self.__lightGroups

    def getGroups(self):
        return self.__groups

    def __saveGroup(self):
        pass

    def __requestLightsFromBridge(self):
        response_code, data = HTTPS.request(HTTPS.GET, self.__address, "/api/" + self.__key + "/lights")
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