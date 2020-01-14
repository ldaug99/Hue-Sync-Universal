from configManager import configManager

class Hue:
    __apiKey = None # API key
    __apiAddress = None # IP address to Bridge
    
    def __init__(self):
        self.run()
        
    def run(self):
        cManager = configManager()
        self.__apiKey = cManager.getKey()
        self.__apiAddress = cManager.getAddress()
        print("Bridge address is {} with key {}".format(self.__apiAddress, self.__apiKey))
