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

address = "https://192.168.87.114/"
#debug/clip.html
#api/newdeveloper
#api
#apiCommand = "api/7wg5y9ytGcQmrjmegai7sxzzcMuFBZxJOlzL8zLL/lights" # Get info on all lights
apiCommand = "api/7wg5y9ytGcQmrjmegai7sxzzcMuFBZxJOlzL8zLL/lights/4/state"

address = address + apiCommand

#PARAMS = {"devicetype":"apiTest#WizardsDesktop"} 

#PARAMS = {"on":True}

from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout


#response = requests.get("https://192.168.87.114/api/7wg5y9ytGcQmrjmegai7sxzzcMuFBZxJOlzL8zLL", verify = False) # Dump all data

#response = requests.get(address, verify = False)
with suppress_stdout():
    for hue in range(0, 65000, 500):
        PARAMS = {"on":True, "sat":254, "bri":254,"hue":hue}
        print(json.dumps(PARAMS))
        response = requests.put(address, json = PARAMS, verify = False)

        #response = requests.post(url = address, json = PARAMS, verify = False)

        #print(response)

        
            
        #if data != None:
        #    print(json.dumps(data, sort_keys=True, indent=4))
        time.sleep(0.00001)



#input("Press Enter to continue...")


#print(https)

#requests.get('https://api.github.com')