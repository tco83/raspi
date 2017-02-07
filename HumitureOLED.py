import time
import datetime
import os
import RPi.GPIO as GPIO

import dht11

from demo_opts import device
from luma.core.virtual import terminal
from PIL import ImageFont

#### CONFIG ZONE ####
dhtpin = 22 # GPIO PIN the DHT11 data pin is connected to
samplingRate = 2 # seconds, how often does data get pulled from DHT11
fontSize = 12

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin=dhtpin)

# initializing OLED display
font = ImageFont.truetype("miscfs_.ttf", fontSize)
oled = terminal(device, font, animate=False)

try:    
    oled.println("################")
    oled.println("# DISPLAY INIT #")
    oled.println("################")
    time.sleep(2)
    oled.clear()
                 
    while True:
        result = instance.read()
        if result.is_valid():
            temp="Temperature: " + str(result.temperature) + "C"
            humid="Humidity: " + str(result.humidity) + "%"
            
            #oled.println(str(datetime.datetime.now()))
            oled.clear()
            oled.println(temp)
            oled.println(humid)
            print("T: %d °C | H: %d %%" % (result.temperature, result.humidity))
            #print("Last valid input: " + str(datetime.datetime.now()))
            #print("Temperature: %d C" % result.temperature)
            #print("Humidity: %d %%" % result.humidity)

        time.sleep(samplingRate)

except KeyboardInterrupt:
    oled.clear()
    print("Ended by user!")
    pass
