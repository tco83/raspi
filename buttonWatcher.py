import RPi.GPIO as GPIO
import time
import os

# Where is the button connected to
buttonPin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# read last state from file
