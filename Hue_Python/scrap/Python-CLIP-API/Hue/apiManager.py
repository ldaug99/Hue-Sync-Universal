import os

class apiManager():
    ### Static class variables ###
    ADDR = "address"
    KEY = "key"

    ### Instance variables ###
    self.__config = {ADDR: None, KEY: None}
    self.__verbose = False

    def __init__(self, **kwargs):
        

        isConfigured = False
        isSaveToFile = False

        self.__verbose = kwargs.get("verbose", False)
        self.__config[ADDR] = kwargs.get("APIaddress", None)
        self.__config[KEY] = kwargs.get("APIkey", None)
        fileName = kwargs.get("configFile", None)
        # Check if address and key is given
        if self.__config[ADDR] != None or self.__config[KEY] != None:
            isConfigured = True
            if self.__verbose:
                print("API address is {}, with key {}".format(self.__config[ADDR], self.__config[KEY]))
        # Check if config file name is given
        if fileName != None:
            if isConfigured:
                
                with open(path, "w") as file:
                    json.dump(data, file)

            

        
            print("API address and key not defined.")

    def run():
        if self.__address == None


    