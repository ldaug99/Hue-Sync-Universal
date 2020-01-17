import configManager
import apiManager
import lightManager

class hue():
    KWARG_VERBOSE = "verbose"
    KWARG_CONFIG = "config"

    def __init__(self, **kwargs):
        # Get variables
        self.__verbose = kwargs.get(hue.KWARG_VERBOSE, False)
        self.__config = kwargs.get(hue.KWARG_CONFIG, {"dir": "default", "file": "config.txt"})
        # Initialize pathages
        # Config manager
        self.__cm = configManager.cm(dir = self.__config["dir"], file = self.__config["file"], verbose = self.__verbose)
        address = self.__cm.loadData("apiMan", "address")
        key = self.__cm.loadData("apiMan", "key")
        # API manager
        self.__am = apiManager.am(address = address, key = key, verbose = True)
        if not self.__am.isReady():
            self.__am.configAPI()
            self.__cm.saveData(self.__am.CONFIG_NAME, self.__am.CONFIG_KEY, self.__am.getAPIconfig)
        # Light manager
        self.__lm = lightManager.lm(verbose = True)
        lightData = self.__cm.loadData(self.__lm.CONFIG_NAME, self.__lm.CONFIG_KEY)
        if lightData != None:
            self.__lm.setConfig(lightData)
        # Done setup
        if self.__verbose:
            print("Module initialization complete")

    def getLights(self):
        return self.__am.getLights()

    def addLightToGroup(self, lightID, group):
        lights = self.getLights()
        for entry in lights:
                if entry["id"] == lightID:
                    if self.__lm.addLightToGroup(lightID, group):
                        self.__cm.saveData(self.__lm.CONFIG_NAME, self.__lm.CONFIG_KEY, self.__lm.getConfig())
                        return True
        return False

    def removeLightFromGroup(self, lightID, group):
        lights = []
        if lightID == "*":
            lightsInGroup = self.__lm.getLightsInGroup(group)
            if lightsInGroup != None:
                for light in lightsInGroup:
                    lights.append(light)
        else:
            lights = lightID
        for light in lights:
            if not self.__lm.removeLightFromGroup(light, group):
                return False
        self.__cm.saveData(self.__lm.CONFIG_NAME, self.__lm.CONFIG_KEY, self.__lm.getConfig())
        return True

    def getGroups(self):
        return(self.__lm.getConfig())

    def setLight(sef, lightID, hue, sat, bri):
        return self.__am.setColor(lightID, hue, sat, bri)

    def setGroupLight(self, group, hue, sat, bri):
        lights = self.__lm.getLightsInGroup(group)
        for lightID in lights:
            self.__am.setColor(lightID, hue, sat, bri)
        if lights == None:
            return False
        return True