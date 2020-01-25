


class lightManager():
    ### Static class variables ###
    CONFIG_NAME = "lightMan"
    CONFIG_KEY = "groups"
    KWARG_CONFIG = "config"
    KWARG_VERBOSE = "verbose"

    CENTER = 0; GCNAME = "center"
    LEFT = 1; GLNAME = "left"
    RIGHT = 2; GRNAME = "right"
    TOP = 3; GTNAME = "top"
    BOTTOM = 4; GBNAME = "bottom"
    GROUPS = [GCNAME, GLNAME, GRNAME, GTNAME, GBNAME]

    def __init__(self, **kwargs):
        self.__lightGroups = {
            lightManager.GROUPS[lightManager.CENTER]: [],
            lightManager.GROUPS[lightManager.LEFT]: [],
            lightManager.GROUPS[lightManager.RIGHT]: [],
            lightManager.GROUPS[lightManager.TOP]: [],
            lightManager.GROUPS[lightManager.BOTTOM]: []
        }
        # Get variables
        config = kwargs.get(lightManager.KWARG_CONFIG, None)
        self.__verbose = kwargs.get(lightManager.KWARG_VERBOSE, False)
        if config != None:
            self.setConfig(config)

    def isReady(self):
        return True

    def setConfig(self, config):
        if config != None:
            for group in config:
                try:
                    self.__lightGroups[group] = config[group]
                except:
                    print("Exception on lightManager() -> setConfig(): Invalid group name")
                    return False
            return True
        else:
            return False

    def getConfig(self):
        return(self.__lightGroups)

    def addLightToGroup(self, lightID, group = GCNAME):
        try:
            if lightID not in self.__lightGroups[group]:
                self.__lightGroups[group].append(lightID)
                return True
            else:
                if self.__verbose:
                    print("Light {} already in group {}".format(lightID, group))
        except:
            print("Exception on lightManager() -> addLightToGroup(): Invalid group name")
        return False

    def removeLightFromGroup(self, lightID, group = GCNAME):
        try:
            if lightID in self.__lightGroups[group]:
                self.__lightGroups[group].remove(lightID)
                return True
            else:
                if self.__verbose:
                    print("Light {} not in group {}".format(lightID, group))
        except:
            print("Exception on lightManager() -> addLightToGroup(): Invalid group name")
        return False

    def getLightsInGroup(self, group):
        if group in self.__lightGroups:
            lights = []
            for light in self.__lightGroups[group]:
                lights.append(light)
            return lights
        else:
            if self.__verbose:
                print("Exception on lightManager() -> addLightToGroup(): Invalid group name")
        return None