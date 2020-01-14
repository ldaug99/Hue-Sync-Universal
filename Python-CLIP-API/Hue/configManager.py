import os
import bridgeFinder
import keySetup

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
        if self.__getFile():
            self.__loadConfig()
        else:
            self.__makeConfig()
        self.__verifyConfig()

    def __getFile(self):
        __path = os.getcwd() # Get working path
        __files = os.listdir(__path) # Get files in path
        for __file in __files:
            if str(__file) == self.__configFileName:
                return True
        return False

    def __loadConfig(self): # Load ip and key from config file
        print("Getting API address and key from config file.")
        __file = open(__configFileName, "r")
        self.__address = __file.readline()
        if self.__address.find("\n") != -1:
            self.__address = self.__address[0: len(self.__address) - 1]
        self.__key = apikeyfile.readline()
        print("API address is {} with key {}".format(self.__address, self.__key))

    def __makeConfig(self): # Make config file, get ip and key and save to file
        __action = input("No config found. Make one? (Yes/No)")
        if __action == "Yes" or __action == "yes" or __action == "y":
            __devices = bridgeFinder.scanNetwork()
            if __devices == None:
                print("No Hue bridge found.") 
                input("Press any key to exit...")
                exit()
            elif len(__devices) > 1:
                print("More then one Hue bridge found, which was unexpected.")
                input("Press any key to exit...")
                exit()
            self.__address = __devices[0] # Save api addres to script variable
            self.__key = getAPIkey(self.__address) # Save key to script variable
            print("Key is: {}".format(self.__key))
            file = open(str(self.__configFileName), "w") # Create config file
            file.write(self.__address) # Save key to fileyes
            file.write(self.__key) # Save key to file
        else:
            input("Press any key to exit...")
            exit()


    def verifyConfig(self, __address, __key):
        print("Verifying address {} and key {}".format(__address, __key))
        if __address == None or __key == None or len(__address) < 1 or len(__key) < 1:
            print("Invalid API address or key.")
            input("Press any key to exit...")
            exit()