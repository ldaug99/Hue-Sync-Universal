import socket
from . import HTTPS

def scanNetwork():
    print("Beginning network scan...")
    hostIP = __getHostIP() # Get host IP address (Note to self: dosen't work with VPN turned on...)
    print("Host IP address is {}".format(hostIP))
    hostIP = __getIPmask(hostIP) # Get mask of address
    if hostIP == None:
        print("Exception on scanNetwork(): Failed to get host IP address.")
        return False
    devices = None
    port = 443
    socket.setdefaulttimeout(0.01) 
    for i in range(2, 256):
        addr = hostIP + "." + str(i)
        result = None
        try:
            print("Scanning IP address {}".format(addr))
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            result = s.connect_ex((addr,port))
        except:
            print("Exception on scanNetwork(): Socket failed to connect to address.")
        if result == 0:
            if __isHue(addr):
                print("Found Hue bridge on address {}".format(addr))
                if devices == None:
                    devices = [addr]
                else:
                    devices.append(addr)
        s.close()
    print("Found Hue bridges on addresses {}".format(devices))
    return devices

def __getHostIP(): # Get host device ip address
    hostIP = None
    hostname = __getHostname()
    if hostname != None:
        try:
            hostIP = socket.gethostbyname(hostname)
        except:
            print("Exception on __getHostIP(): Failed to get host IP address.")
    return hostIP

def __getHostname(): # Get host device name
    hostname = None
    try:
        hostname = socket.gethostname()
    except:
        print("Exception on __getHostname(): Failed to get hostname.")
    return hostname

def __getIPmask(hostIP):
    last_pos = hostIP.rfind(".")        
    return hostIP[0:last_pos]

def __isHue(address): # Return true if device is a Hue bridge
    response = __getDescription(address)
    if (response.find("Philips hue") != -1):
        return True
    return False

def __getDescription(address): # Get description from device
    timeout = 100 # Maksimum time to wait for reply
    response_code, data = HTTPS.request(HTTPS.GET, address, "/description.xml", timeout = timeout, verbose = False, dataType = "text")
    return data