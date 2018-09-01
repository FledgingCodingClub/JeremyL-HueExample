#!/usr/bin/env python

from os import path
from qhue import Bridge, QhueException, create_new_username
from sys import argv
import weather

# the IP address of your bridge
BRIDGE_IP = "192.168.1.242"


# the path for the username credentials file
CRED_FILE_PATH = "qhue_username.txt"

def main():
    temp = None
    if len(argv) == 2:
        temp = int(argv[1])
    else:
        temp = weather.WeatherCom().temperature()
    
    
    # check for a credential file
    if not path.exists(CRED_FILE_PATH):

        while True:
            try:
                username = create_new_username(BRIDGE_IP)
                break
            except QhueException as err:
                print("Error occurred while creating a new username: {}".format(err))

        # store the username in a credential file
        with open(CRED_FILE_PATH, "w") as cred_file:
            cred_file.write(username)

    else:
        with open(CRED_FILE_PATH, "r") as cred_file:
            username = cred_file.read()

    # create the bridge resource, passing the captured username
    bridge = Bridge(BRIDGE_IP, username)

    # create a lights resource
    lights = bridge.lights
    
    if temp < 30:
        lights[1].state(bri=100,hue=46920)
        #print "Less than 30"
    elif temp <= 70:
        lights[1].state(bri=100,hue=56100)
        #print "Greater than or eq to 30 and <=70"
    elif temp <= 120:
        lights[1].state(bri=100,hue=65280)
        #print "LT or EQ 120"
    else:
        print("Error: Temperature out of Range")
    
    # query the API and print the results
    #print(lights())

if __name__ == "__main__":
    main()
