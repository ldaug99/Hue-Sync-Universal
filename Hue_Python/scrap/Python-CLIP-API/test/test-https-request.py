#import os
#import certifi
#import urllib3
import requests
import json
import time
import sys

#[{'success': {'username': '7wg5y9ytGcQmrjmegai7sxzzcMuFBZxJOlzL8zLL'}}]

#path = os.getcwd()
#path = path + "\\" + "CLIP-API-Debugger-Certificate.cer"

#https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

#response = requests.get('https://192.168.87.114/debug/clip.html', verify = path)
#response = requests.get('https://192.168.87.114/debug/clip.html', verify = certifi.where())

#response = https.requests('GET', 'https://192.168.87.114/debug/clip.html')

#address = "https://192.168.87.114/"
#debug/clip.html
#api/newdeveloper
#api
#apiCommand = "api/7wg5y9ytGcQmrjmegai7sxzzcMuFBZxJOlzL8zLL/lights" # Get info on all lights
#apiCommand = "api/7wg5y9ytGcQmrjmegai7sxzzcMuFBZxJOlzL8zLL/lights/4/state"

#address = address + apiCommand

#PARAMS = {"devicetype":"apiTest#WizardsDesktop"} 

#PARAMS = {"on":True}

#from contextlib import contextmanager
#import sys, os

#@contextmanager
#def suppress_stdout():
#    with open(os.devnull, "w") as devnull:
#        old_stdout = sys.stdout
#        sys.stdout = devnull
#        try:  
#            yield
#        finally:
#            sys.stdout = old_stdout

lightID = "8"
bri = "241"
sat = "241"
hue = "50000"


#address = "https://192.168.87.183/api/jVfvoEykjhjr5JU448bac1XruOG-jYVMW1s6WCAY/lights/"

#address = "https://192.168.1.57/api/h0Ov2zL9X7i7plHOBc2HTH8p4n0SAjxyjpSfe6fv/lights/4/state"


address = "https://192.168.87.114/api/7wg5y9ytGcQmrjmegai7sxzzcMuFBZxJOlzL8zLL/lights/2/state"


#params = {"bri": int(bri), "hue": int(hue), "on": True, "sat": int(sat), "transitiontime": 1}

params = {"on": True, "xy": [0.25, 0.70], "bri": 255, "transitiontime": 0}

response = requests.put(address, json = params, verify = False)

#no = False
#response = requests.get(address, verify = False) # Dump all data
try:
    data = response.json()
    print(json.dumps(data, sort_keys=True, indent=3))
except:
    pass

    

#response = requests.get(address, verify = False)
#with suppress_stdout():
#    for hue in range(0, 65000, 500):
#        PARAMS = {"on":True, "sat":254, "bri":254,"hue":hue}
#        print(json.dumps(PARAMS))
#        response = requests.put(address, json = PARAMS, verify = False)

        #response = requests.post(url = address, json = PARAMS, verify = False)

        #print(response)

        
            
        #if data != None:
        #    print(json.dumps(data, sort_keys=True, indent=4))
#        time.sleep(0.00001)




#lights = None

#for i in range(1, len(data) + 1):
#    name = None
#    try:
#        name = data[str(i)]["name"]
#    except:
#        pass
#    light = {"id": str(i), "name": name}
#    if lights == None:
#        lights = [light]
#    else:
#        lights.append(light)
#print(lights)


#input("Press Enter to continue...")


#print(https)

#requests.get('https://api.github.com')