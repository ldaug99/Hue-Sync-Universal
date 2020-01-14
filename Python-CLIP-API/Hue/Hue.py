from configManager import configManager
from lightManager import lightManager

class Hue:
    __apiKey = None # API key
    __apiAddress = None # IP address to Bridge
    __cManager = None
    __lManager = None

    def __init__(self):
        self.run()
        
    def run(self):
        self.__cManager = configManager()
        self.__apiKey = self.__cManager.getKey()
        self.__apiAddress = self.__cManager.getAddress()
        print("Bridge address is {} with key {}".format(self.__apiAddress, self.__apiKey))
        if self.__apiAddress != None and self.__apiKey != None:
            self.__lManager = lightManager(self.__apiAddress, self.__apiKey, verbose = True)
            lights = self.__lManager.getLights()
        self.waitForCommand()
            
    def getAddress(self):
        return self.__apiAddress
    
    def getKey(self):
        return self.__apiKey
    
    def waitForCommand(self):
        while 1==1:
            command = input("Input a command: ")
            self.__processCommand(command)

    def __processCommand(self, command):
        switcher = {
            "help": self.__comHelp,
            "add": self.__comAddLight,
            "remove": self.__comRemoveLight,
            "lights": self.__comLights,
            "colorL": self.__comColorL
        }
        function = switcher.get(command, self.__comInvalid)
        function()

    def __comHelp(self):
        print("     Avaliable commands:")
        print("         help - Prints help.")
        print("         add - Adds light to group.")
        print("         remove - Removes light from group.")
        print("         lights - Prints avalibale lights.")
        print("         colorL - Set color of light or group.")
        print("         colorG - Set color of light or group.")
        print(" ")
        pass
            
    def __comAddLight(self):
        self.__comLights()
        lightID = input("Input light ID: ")
        group = input("Input light group: ")
        if group in self.__lManager.getGroups():
            self.__lManager.addLight(lightID, group)
        print(self.__lManager.getGroupSetup())
            
    def __comRemoveLight(self):
        lightID = input("Input light ID: ")
        pass

    def __comColorL(self):
        lightID = input("Input light ID: ")
        sat = input("Input light saturation: ")
        bri = input("Input light brightness: ")
        hue = input("Input light hue: ")
        self.__lManager.setColor(lightID, hue, sat, bri)

    def __comColorG(self):
        groupID = input("Input group name: ")
        pass

    def __comLights(self):
        print("     Avaliable lights: {}".format(self.__lManager.getLights()))
        print(" ")
        pass

    def __comInvalid(self):
        print("     Invalid command.")
        print(" ")
        self.__comHelp()