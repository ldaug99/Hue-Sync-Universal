

class apiManager:
    ADDR = "address"
    KEY = "key"
    self.__config = {ADDR: None, KEY: None}
    self.__address = None
    self.__key = None

    def __init__(self, **kwargs):
        self.__config[ADDR] = kwargs.get("APIaddress", None)
        self.__config[KEY] = kwargs.get("APIkey", None)
        if self.__config[ADDR] == None or self.__config[KEY] == None:
            print("API address and key not defined.")

    def run():
        if self.__address == None

        