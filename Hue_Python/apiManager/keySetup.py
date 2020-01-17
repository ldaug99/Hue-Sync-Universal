from . import HTTPS
import time

def getAPIkey(address, **kwargs):
    '''
    Gets API key from Hue bridge on the passed IP address.    

    Parameters:
    address: IP address of bridge.
    (optional) deviceName: Name to register with the bridge.
    (optional) retrys: Maximum number of retrys.
    (optional) delay: Delay between each retry.

    Returns:
    string or None: API key from bridge, or None on fault.
    '''
    __key = None # Presume key is None
    __name = kwargs.get('deviceName', None) # Get optional input "deviceName"
    __retrys = kwargs.get('retrys', 100)
    __delay = kwargs.get('delay', 10) 
    __retry_num = kwargs.get('__retry_num', 0)
    if __name == None:
        __name = input("Input device name: ")
    params = {"devicetype":__name} # JSON paramaters to send
    response_code, data = HTTPS.request(HTTPS.POST, address, "/api", params = params) # Send post reqiest to /api with parameters
    if response_code == 200: # Check if api got message, code 200 indicates succesfull request
        if data != None: # Check if data is none
            if "error" in data[0]: #and 101 in data[0]["error"]: # If link button not pressed
                __retry_num = __retry_num + 1 # Increment retry attempt counter
                if __retry_num > __retrys:
                    print("Maximum number of retrys reached. Stopping...")
                    return None
                print("Press link button on Hue Bridge")
                #input("Press enter to retry connection") # Wait for input
                time.sleep(__delay) # Sleep for 5 seconds
                __key = getAPIkey(address, deviceName = __name) # Retry function
            elif "success" in data[0]: # If successfull request
                try:
                    __key = data[0]["success"]["username"] # Save api key
                    print("Got API key: {}".format(__key))
                except:
                    pass
        else:
            print("Exception on getAPIkey(): Method didn't return data, which was unexpected")
    else:
        print("Exception on getAPIkey(): Method returned response code {}, which was unexpected.".format(response_code))
    return __key