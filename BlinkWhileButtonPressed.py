import RPi.GPIO as GPIO
import time

# Adressierungs-Schema der PINs festlegen
GPIO.setmode(GPIO.BOARD)

# Pin11,13,15 als Output definieren (LEDs)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

# PIN 12 als Input-PIN mit Default True (PUD_UP) definieren.
# der Druck des Buttons zieht dann runter (False)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Farbzuordnung LEDs (bessere Lesbarkeit Code)
red=11
yellow=13
green=15

# Define flash-sleep time
sleeptime = 0.3

while True:
    # Read button push status
    input_state = GPIO.input(12)

    while input_state == False:
        # Do as long as Button is pushed
        GPIO.output(red, GPIO.HIGH)
        time.sleep(sleeptime)
        GPIO.output(red, GPIO.LOW)

        GPIO.output(yellow, GPIO.HIGH)
        time.sleep(sleeptime)
        GPIO.output(yellow, GPIO.LOW)

        GPIO.output(green, GPIO.HIGH)
        time.sleep(sleeptime)
        GPIO.output(green, GPIO.LOW)
        time.sleep(sleeptime)
        GPIO.output(green, GPIO.HIGH)
        time.sleep(sleeptime)
        GPIO.output(green, GPIO.LOW)

        input_state = GPIO.input(12)
