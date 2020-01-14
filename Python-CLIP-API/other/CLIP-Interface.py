import os
import requests
import json





filename = "config.txt"
apiAddress = ""
apiKey = ""


def readInput(message):
    return input(message)



def setIPaddress(ipAddress):
    apiAddress = ipAddress

def setAPIkey(key):
    apiKey = key




def getAPIkey(ipAddres, **kwargs):
    __name = kwargs.get('deviceName', None)
    __key = kwargs.get('apiKey', None)
    if __name == None:
        __name = input("Input device name: ")
    params = {"devicetype":__name} # JSON paramaters to send
    #response_code, data = sendRequest(POST, ipAddres, "/api", params = params) # Send post reqiest to /api with parameters
    response_code = 200
    data = [{"success":{"username":"7wg5y9ytGcQmrjmegai7sxzzcMuFBZxJOlzL8zLL"}}]
    if response_code == 200: # Check if api got message, code 200 indicates succesfull request
        if data != None: # Check if data is none
            if "error" in data[0]: #and 101 in data[0]["error"]: # If link button not pressed
                print("Press link button on Hue Bridge")
                input("Press enter to retry connection") # Wait for input
                getAPIkey(ipAddres, deviceName = __name, apiKey = __key) # Retry function
            elif "success" in data[0]: # If successfull request
                try:
                    __key = data[0]["success"]["username"] # Save api key
                    print("Got API key: {}".format(__a__keypiKey))
                except:
                    pass
        else:
            print("Method didn't return data, which was unexpected")
    else:
        print("Method returned response code {}, which was unexpected.".format(getResponseCode(response)))
    return __key





#def getIPmask(hostIP):
#    found_last = False
#    last_pos = 0
#    while(found_last):
#        point = hostIP.find(".", last_pos)
#        last_pos = point
#        if (hostIP.find(".", last_pos) == -1)
#            found_last = True
#    IPmask = hostIP.
#    return 










#while 1==1: # Main loop
#    loadConfig() # Load config

#scanNetwork()
#print(getIPmask("192.168.1.87"))
getConfig()
