import main

class cli():
    def __init__(self):
        self.__hue = main.hue(verbose = True, config = {"dir": "default", "file": "l_config.txt"})
        #self.__hue = main.hue(verbose = True)
        self.__hue.getLights()
        self.doRun = True
        self.showFrame = False
        self.run()

    def run(self):
        self.waitForCommand()

    def waitForCommand(self):
        while self.doRun:
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
            "groups": self.__commGroups,
            "start": self.__commStart,
            "stop": self.__commStop,
            "fs": self.__commFs,
            "tf": self.__commFrame,
            "exit": self.__commExit
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
        print("         start  - Start color capture.")
        print("         stop   - Stop color capture.")
        print("         fs     - Set capture frequency in Hz.")
        print("         tf     - Toggle show frame.")
        print("         exit   - Exit script.")
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
        R = input("Input light red: ")
        G = input("Input light green: ")
        B = input("Input light blue: ")
        print(self.__hue.setLight(lightID, R, G, B))
        print(" ")

    def __comColorG(self):
        print(self.__hue.getGroups())
        group = input("Input group name: ")
        R = input("Input light red: ")
        G = input("Input light green: ")
        B = input("Input light blue: ")
        print(self.__hue.setGroupLight(group, R, G, B))
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
    
    def __commStart(self):
        print("     Starting color capture...")
        self.__hue.startColorCapture()
        print(" ")

    def __commStop(self):
        print("     Stopping color capture...")
        self.__hue.stopColorCapture()
        print(" ")

    def __commFrame(self):
        if self.showFrame:
            self.showFrame = False
            self.__hue.showFrame(self.showFrame)
        else:
            self.showFrame = True
            self.__hue.showFrame(self.showFrame)
        print("Showing frame {}".format(self.showFrame))
        print(" ")

    def __commFs(self):
        fs = input("Input update frequency: ")
        self.__hue.setUpdateFrequency(fs)
        print(" ")

    def __commExit(self):
        print("     Exiting script...")
        self.__hue.cleanup()
        self.doRun = False

cli()