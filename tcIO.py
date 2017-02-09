# importing all necessary libraries
import time
import RPi.GPIO as GPIO

import dht11 # The dht11 humiture sensor

# Everything needed for the OLED
from demo_opts import device
from luma.core.virtual import terminal
from luma.core.render import canvas
from PIL import ImageFont
        
def initGPIO(m=GPIO.BCM, warnings=False):
    GPIO.setwarnings(warnings)
    GPIO.setmode(m)
    GPIO.cleanup()

def initOLED(fontName="Minecraft.ttf", fontSize=12, animateDisplay=False):
    fontHandler = ImageFont.truetype(fontName, fontSize)
    return terminal(device, fontHandler, animate=animateDisplay)
        
        
