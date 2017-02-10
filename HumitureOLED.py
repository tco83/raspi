import time
import datetime
import os
import RPi.GPIO as GPIO

import dht11

from demo_opts import device
from luma.core.virtual import terminal
from luma.core.render import canvas
from PIL import ImageFont

#### CONFIG ZONE ####
samplingRate = 2 # seconds, how often does data get pulled from DHT11
fontName = "upheavtt.ttf"
fontSize = 40

def init():
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

def initButton(pin=18):
    # initialize the Button to on/off display
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buttonPressed(pin=18):
    input_state = GPIO.input(pin)
    if input_state == False:
        print("GEDRÜCKT!")
        return True
    elif input_state == True:
        return False

def DHT(pin=22):
    # read data using pin 14
    instance = dht11.DHT11(pin=pin)
    return instance

def displayData(device, font, temp, humid):
    with canvas(device) as draw:
        draw.text((0,0), str(temp)+"C", font=font, fill="white")
        draw.text((0,32), str(humid)+"%", font=font, fill="white")

def displayClear(device):
    with canvas(device) as draw:
        draw.rectangle((0,0,device.width, device.height), fill="black")

def main(outputHandler):
    init()
    initButton()

    oledActive = False
    
    dhtInstance = DHT()
    fontHandler = ImageFont.truetype(fontName, fontSize)

    while True:
        # Check if button is pressed and oled state needs change
        if buttonPressed() == True and oledActive == False:
            oledActive = True
        elif buttonPressed() == True and oledActive == True:
            oledActive = False
            displayClear(device)
            
        res = dhtInstance.read()
        if res.is_valid():
            temp = res.temperature
            humid = res.humidity
            outputHandler.write(time.strftime("%d.%m.%Y %H:%M:%S") +";"+ str(temp) +";"+ str(humid) + "\n")
            outputHandler.flush()
            print(time.strftime("%d.%m.%Y %H:%M:%S") +";"+ str(temp) +";"+ str(humid))
            if oledActive == True:
                displayData(device, fontHandler, temp, humid)
            
        time.sleep(samplingRate)
        
if __name__ == "__main__":
    try:
        outputFileName = "out_"+str(round(time.time()))+".csv"
        outputHandler = open(outputFileName, mode="a")
        main(outputHandler)
    except KeyboardInterrupt:
        displayClear(device)
        outputHandler.close()
        print("Ended by user (Strg+C)!")
        print("Display cleared ...")
        print("Filehandlers closed ...")
        pass

