import main

class cli():
    def __init__(self):
        self.__hue = main.hue(verbose = True, config = {"dir": "default", "file": "l_config.txt"})
        self.run()

    def run(self):
        self.waitForCommand()

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
            "colorL": self.__comColorL,
            "colorG": self.__comColorG,
            "groups": self.__commGroups
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
        print("         groups - Prints lights in groups.")
        print(" ")
        pass

    def __comAddLight(self):
        self.__comLights()
        lightID = input("Input light ID: ")
        group = input("Input light group: ")
        print(self.__hue.addLightToGroup(lightID, group))
        print(" ")
            
    def __comRemoveLight(self):
        print(self.__hue.getGroups())
        lightID = input("Input light ID: ")
        group = input("Input light group: ")
        print(self.__hue.removeLightFromGroup(lightID, group))
        print(" ")

    def __comColorL(self):
        lightID = input("Input light ID: ")
        hue = input("Input light hue: ")
        sat = input("Input light saturation: ")
        bri = input("Input light brightness: ")
        print(self.__hue.setColor(lightID, hue, sat, bri))
        print(" ")

    def __comColorG(self):
        print(self.__hue.getGroups())
        group = input("Input group name: ")
        hue = input("Input light hue: ")
        sat = input("Input light saturation: ")
        bri = input("Input light brightness: ")
        print(self.__hue.setGroupLight(group, hue, sat, bri))
        print(" ")

    def __comLights(self):
        print("     Avaliable lights: {}".format(self.__hue.getLights()))
        print(" ")
        pass

    def __comInvalid(self):
        print("     Invalid command.")
        print(" ")
        self.__comHelp()
    
    def __commGroups(self):
        print("     Groups {}".format(self.__hue.getGroups()))
        print(" ")
    
cli()