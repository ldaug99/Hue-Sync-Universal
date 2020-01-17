import os
import json

class configManager:
    ### Static class variables ###
    DEFAULT_CONFIG_NAME = "config.txt"
    FILE_SUBFOLDER = "//config"
    KWARG_DIR = "dir"
    KWARG_NAME = "file"
    KWARG_VERBOSE = "verbose"
    KWARG_DEFAULT = "default"

    # Initialization
    def __init__(self, **kwargs):
        # Get variables
        self.__path = {configManager.KWARG_DIR: kwargs.get(configManager.KWARG_DIR, None), configManager.KWARG_NAME: kwargs.get(configManager.KWARG_NAME, None)}
        self.__verbose = kwargs.get(configManager.KWARG_VERBOSE, False)
        # Check if path is given:
        if self.__path[configManager.KWARG_DIR] == None or self.__path[configManager.KWARG_DIR] == configManager.KWARG_DEFAULT:
            if self.__verbose:
                print("No directory given, using default.")
            __script = os.path.realpath(__file__)
            __dir = os.path.dirname(__script)
            self.__path[configManager.KWARG_DIR] = __dir + configManager.FILE_SUBFOLDER + "\\"
        if self.__verbose:
            print("Using directory {}".format(self.__path[configManager.KWARG_DIR]))
        # Check if filename is given
        if self.__path[configManager.KWARG_NAME] == None:
            if self.__verbose:
                print("No filename given, using default.")
            self.__path[configManager.KWARG_NAME] = configManager.DEFAULT_CONFIG_NAME
        if self.__verbose:
            print("Using filename {}".format(self.__path[configManager.KWARG_NAME]))

    def loadData(self, module, key):
        fileData = self.__getDataFromFile()
        entryData = None
        if fileData != None:
            if module in fileData:
                if key in fileData[module]:
                    entryData = fileData[module][key]
                    if self.__verbose:
                        print("Found data {} at module {} and key {}".format(entryData, module, key))
                else:
                    if self.__verbose:
                        print("Exception on configManager() -> __loadFromFile(): Key not found in data.")
            else:
                if self.__verbose:
                    print("Exception on configManager() -> __loadFromFile(): Module name not found in data.")
        else:
            if self.__verbose:
                print("No config file found.")
        return entryData

    def saveData(self, module, key, data):
        fileData = self.__getDataFromFile()
        if fileData != None:
            if module in fileData:
                moduleData = fileData[module]
                moduleData[key] = data
                fileData[module] = moduleData
            else:
                fileData[module] = {key: data}
        else:
            fileData = {module: {key: data}}
        result = False
        with open(self.__path[configManager.KWARG_DIR] + self.__path[configManager.KWARG_NAME], "w") as file:
            result = json.dump(fileData, file, indent=4, sort_keys=True)
        if result == None:
            return True
        else:
            return False

    def __getDataFromFile(self):
        fileData = None
        try:
            with open(self.__path[configManager.KWARG_DIR] + self.__path[configManager.KWARG_NAME], "r") as file:
                try:
                    fileData = json.load(file)
                except:
                    if self.__verbose:
                        print("Config file empty.")
        except:
            if self.__verbose:
                print("No config file found.")
        return fileData