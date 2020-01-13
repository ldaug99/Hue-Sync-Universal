import os
import requests
import json
import socket

GET = 0; PUT = 1; POST = 2; DELETE = 3;


filename = "config.txt"
apiAddress = ""
apiKey = ""


def readInput(message):
    return input(message)



def setIPaddress(ipAddress):
    apiAddress = ipAddress

def setAPIkey(key):
    apiKey = key

def sendRequest(rtype = 0, ipAddress = apiAddress, apiCommand = "api", **kwargs):
    verify = kwargs.get('verify', False)
    response = "Unknown type"
    ipAddress = "https://" + ipAddress + apiCommand
    params = None
    if rtype == GET: # Get method
        try: 
            response = requests.get(ipAddress, verify = verify)
        except:
            pass
    elif rtype == PUT: # Put method
        try: 
            params = kwargs.get('params', {})
            response = requests.put(ipAddress, json = params, verify = verify)
        except:
            pass
    elif rtype == POST: # Post method
        try: 
            params = kwargs.get('params', {})
            response = requests.post(ipAddress, json = params, verify = verify)
        except:
            pass
    elif rtype == DELETE: # Delete method
        response = "Unallowed method"
        #params = kwargs.get('params', {})
        #response = requests.delete(ipAddress, json = params, verify = verify)
    #else:
    response_code = getResponseCode(response) # Get response code
    data = getData(response) # Get data
    print("Sendt request type {} to address {}, with data {}".format(rtype, ipAddress, params))
    print("Request returned response {} and data {}".format(response_code,data))
    return response_code, data # Return response and data

def getData(response): # Check for data in response
    data = None
    try:
        data = response.json()
    except ValueError:
        print("No data returned.")
    return data

def getConfig(): # Load config gile
    path = os.getcwd() # Get working path
    files = os.listdir(path) # Get files in path
    found_file = False # Check if file found
    for each_file in files:
        if str(each_file) == filename:
            found_file = True
    if not found_file:
        makeConfig()
    loadConfig() 
    verifyConfig()

def makeConfig(): # Make config file, get ip and key and save to file
    action = input("No config found. Make one? (Yes/No)")
    if action == "Yes" or action == "yes" or action == "y":
        devices = scanNetwork()
        if devices == None:
            print("No Hue bridge found.") 
            input("Press any key to exit...")
            exit()
        elif len(devices) > 1:
            print("More then one Hue bridge found, which was unexpected.")
            input("Press any key to exit...")
            exit()
        __apiAddress = devices[0] # Save api addres to script variable
        __apiKey = getAPIkey(__apiAddress) # Save key to script variable
        print("Key is: {}".format(__apiKey))
        verifyConfig(__apiAddress, __apiKey)
        apikeyfile = open(str(filename), "w") # Create config file
        apikeyfile.write(__apiAddress) # Save key to fileyes
        apikeyfile.write(__apiKey) # Save key to file
    else:
        input("Press any key to exit...")
        exit()

def loadConfig(): # Load ip and key from config file
    print("Getting API address and key from config file.")
    apikeyfile = open(filename, "r")
    __apiAddress = apikeyfile.readline()
    if __apiAddress.find("\n") != -1:
        setIPaddress(__apiAddress[0: len(__apiAddress) - 1])
    setAPIkey(apikeyfile.readline())
    print("API address is {} with key {}".format(apiAddress, apiKey))

def verifyConfig(__address, __key):
    print("Verifying address {} and key {}".format(__address, __key))
    if __address == None or __key == None or len(__address) < 1 or len(__key) < 1:
        print("Invalid API address or key.")
        input("Press any key to exit...")
        exit()

def getAPIkey(ipAddres, **kwargs):
    __name = kwargs.get('deviceName', None)
    __key = kwargs.get('apiKey', None)
    if __name == None:
        __name = input("Input device name: ")
    params = {"devicetype":__name} # JSON paramaters to send
    response_code, data = sendRequest(POST, ipAddres, "/api", params = params) # Send post reqiest to /api with parameters
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

def getResponseCode(response): # Get response code form requests, or None on fault
    code = None
    try:
        code = response.status_code
    except:
        pass
    return code

def scanNetwork():
    print("Beginning network scan...")
    hostIP = getHostIP() # Get host IP address (Note to self: dosen't work with VPN turned on...)
    print("Host IP address is {}".format(hostIP))
    hostIP = getIPmask(hostIP) # Get mask of address
    if hostIP == None:
        print("Scan aborted.")
        return False
    devices = None
    port = 443
    socket.setdefaulttimeout(0.005) 
    for i in range(2, 256):
        addr = hostIP + "." + str(i)
        result = None
        try:
            print("Scanning IP address {}".format(addr))
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            result = s.connect_ex((addr,port))
        except:
            print("Socket failed to connect to address.")
        if result == 0:
            if isHue(addr):
                print("Found Hue bridge on address {}".format(addr))
                if devices == None:
                    devices = [addr]
                else:
                    devices.append(addr)
        s.close()
    print("Found Hue bridges on addresses {}".format(devices))
    return devices

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

def getIPmask(hostIP):
    last_pos = hostIP.rfind(".")        
    return hostIP[0:last_pos]

def getHostname(): # Get host device name
    hostname = None
    try:
        hostname = socket.gethostname()
    except:
        print("Failed to get hostname.")
    return hostname

def getHostIP(): # Get host device ip address
    hostIP = None
    hostname = getHostname()
    if hostname != None:
        try:
            hostIP = socket.gethostbyname(hostname)
        except:
            print("Failed to get host IP address.")
    return hostIP

def getDescription(addr): # Get description from device
    timeout = 1
    addr = "https://" + addr + "/description.xml"
    response = None
    try:
        response = requests.get(addr, verify = False, timeout = timeout)
    except:
        pass
    return response

def isHue(addr): # Return true if device is a Hue bridge
    response = getDescription(addr)
    try:
        description = response.text
    except:
        return False
    if (description.find("Philips hue") != -1):
        return True
    return False

#while 1==1: # Main loop
#    loadConfig() # Load config

#scanNetwork()
#print(getIPmask("192.168.1.87"))
getConfig()
