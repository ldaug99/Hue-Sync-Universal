import os
import bridgeFinder
from keySetup import *

class configManager():
    __configFileName = "config.txt" # Config file name
    __address = None
    __key = None
    
    def __init__(self):
        self.__getConfig()
    
    def getAddress(self):
        return self.__address

    def getKey(self):
        return self.__key

    def __getConfig(self): # Load config gile
        isFile, path = self.__getFile()
        if isFile:
            self.__loadConfig(path)
        else:
            self.__makeConfig(path)
        self.__verifyConfig(self.__address, self.__key)

    def __getFile(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) 
        root = None
        for root, dirs, files in os.walk(dir_path): 
            for file in files:  
                if str(file) == self.__configFileName:
                    return True, root + "\\" + file
        
        #path = os.path.abspath(self.__file__) # Get working path
        #files = os.listdir(path) # Get files in path
        #print("Paths is {}".format(path))
        #for file in files:
        #    if str(file) == self.__configFileName:
        #        return True
        
        return False, root + "\\" + self.__configFileName

    def __loadConfig(self, path): # Load ip and key from config file
        print("Getting API address and key from config file.")
        with open(path, "r") as file:
            data = json.load(file)
        try:
            self.__address = data["address"]
            self.__key = data["key"]
            return True
        except:
            print("Exception on __loadConfig(): Invalid config file format.")
            return False

    def __makeConfig(self, path): # Make config file, get ip and key and save to file
        action = input("No config found. Make one? (Yes/No)")
        if action == "Yes" or action == "yes" or action == "y":
            devices = bridgeFinder.scanNetwork()
            if devices == None:
                print("No Hue bridge found.") 
                input("Press any key to exit...")
                exit()
            elif len(devices) > 1:
                print("More then one Hue bridge found, which was unexpected.")
                input("Press any key to exit...")
                exit()
            self.__address = devices[0] # Save api addres to script variable
            self.__key = getAPIkey(self.__address) # Save key to script variable
            print("Key is: {}".format(self.__key))
            data = {"address": self.__address, "key": self.__key}
            with open(path, "w") as file:
                json.dump(data, file)
        else:
            input("Press any key to exit...")
            exit()

    def __verifyConfig(self, __address, __key):
        print("Verifying address {} and key {}".format(__address, __key))
        if __address == None or __key == None or len(__address) < 1 or len(__key) < 1:
            print("Invalid API address or key.")
            input("Press any key to exit...")
            exit()
        else:
            print("Ok")