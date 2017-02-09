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
    dhtInstance = DHT()
    fontHandler = ImageFont.truetype(fontName, fontSize)

    while True:
        res = dhtInstance.read()
        if res.is_valid():
            temp = res.temperature
            humid = res.humidity
            outputHandler.write(time.strftime("%d.%m.%Y %H:%M:%S") +";"+ str(temp) +";"+ str(humid) + "\n")
            outputHandler.flush()
            print(time.strftime("%d.%m.%Y %H:%M:%S") +";"+ str(temp) +";"+ str(humid))
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

