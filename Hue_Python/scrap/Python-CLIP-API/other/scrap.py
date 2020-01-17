def scanNetwork():
    hostIP = getHostIP()
    if hostIP == None:
        print("Scan aborted.")
        return False
    devices = None
    timeout = 0.001
    for i in range(2, 256):
        addr = "https://192.168.87." + str(i) + "/description.xml"
        try:
            response = requests.get(addr, verify = False, timeout = timeout)
        except:
            continue
        if response.status_code == response.ok:
            if isHue(response):
                if devices == None:
                    devices = {addr}
                else:
                    devices.add(addr)
                print("Found device on address {}.".format(addr))
        requests.close()
    print(devices)
    input("Done scanning")

def isHue(response): # Return true if device is a Hue bridge
    try:
        description = response.text
        if (description.find("Philips hue")):
            return True
    except:
        pass
    return False