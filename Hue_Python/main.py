import configManager
import apiManager
import lightManager
import camManager
import mainThread
import time

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
        if address != None and key != None:
            self.__am = apiManager.am(address = address, key = key, verbose = self.__verbose, bri = 254)
        else:
            self.__am = apiManager.am(verbose = self.__verbose)
        if not self.__am.isReady():
            self.__am.configAPI()
            apiConfig = self.__am.getAPIconfig()
            self.__cm.saveData(self.__am.CONFIG_NAME, self.__am.CONFIG_ADDR, apiConfig[self.__am.CONFIG_ADDR])
            self.__cm.saveData(self.__am.CONFIG_NAME, self.__am.CONFIG_KEY, apiConfig[self.__am.CONFIG_KEY])
        # Light manager
        self.__lm = lightManager.lm(verbose = self.__verbose)
        lightData = self.__cm.loadData(self.__lm.CONFIG_NAME, self.__lm.CONFIG_KEY)
        if lightData != None:
            self.__lm.setConfig(lightData)
        # Camera manager
        self.__wm = camManager.wm(verbose = self.__verbose)
        if not self.__wm.isReady():
            if not self.__wm.retryOpen():
                print("Exception on hue() -> __init__(): Unable to start camera manager.")
                return False
        # Main thread
        self.__mt = mainThread.mt(self.__lm, self.__am, self.__wm, verbose = self.__verbose)
        self.__mt.setName("mainThread")
        self.__mt.start()
        time.sleep(0.5)
        if not self.__mt.isRunning():
            try:
                self.__mt.join()
            except:
                pass
            print("Exception on hue() -> __init__(): Unable to start main thread.")
        # Done setup
        if self.__verbose:
            print("Module initialization complete")

    def cleanup(self):
        self.__wm.release()
        self.__mt.stop()
        self.__mt.join()

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

    def setLight(self, lightID, r, g, b):
        return self.__am.setColor(lightID, r, g, b)

    def setGroupLight(self, group, r, g, b):
        lights = self.__lm.getLightsInGroup(group)
        for lightID in lights:
            self.__am.setColor(lightID, r, g, b)
        if lights == None:
            return False
        return True

    def setUpdateFrequency(self, fs):
        if self.__mt.isRunning():
            self.__mt.setFs(int(fs))
        else:
            print("Exception on hue() -> setUpdateFrequency(): mainThread not running.")

    def startColorCapture(self):
        if self.__mt.isRunning():
            self.__mt.startCapture()
        else:
            print("Exception on hue() -> startColorCapture(): mainThread not running.")

    def stopColorCapture(self):
        if self.__mt.isRunning():
            self.__mt.stopCapture()
        else:
            print("Exception on hue() -> stopColorCapture(): mainThread not running.")
    
    def showFrame(self, state):
        self.__wm.showFrame(state)