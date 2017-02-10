import time
import RPi.GPIO as GPIO
import multiprocessing

import dht11

from demo_opts import device
#from luma.core.virtual import terminal
from luma.core.render import canvas
from PIL import ImageFont

def initGPIO():
    ''' Initialize GPIO '''
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    
def buttonGuard(pin=18, sampleRate, q):
    ''' Look for button press on pin and write change in state to queue q '''
    # initialize the Button to on/off display
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Determine base setting
    buttonPressed = False
    
    # Get into loop
    while True:
        currentInput = GPIO.input(pin) # read current value from PIN

        if currentInput == False:
            # Button pressed right now
            buttonPressed = True
            
        elif currentInput == True:
            # Button not pressed right now
            # Check if Button was just "lifted" and queue is empty
            if buttonPressed == True and q.empty():
                q.put(True)

            buttonPressed = False
            
        time.sleep(sampleRate)

def readDHT(pin=22, sampleRate, q):
    ''' Read the values of the DHT and write result to result queue q '''
    # Create instance
    dhtsensor = dht11.DHT11(pin=pin)
    
    # get into loop
    while True:
        # read from Sensor
        res = dhtsensor.read()

        # if reading delivered valid results write them to the result queue
        if res.is_valid():
            # Create and format result variables
            timestamp = time.strftime("%d.%m.%Y %H:%M:%S")
            temperature = res.temperature
            humidity = res.humidity

            # Write tuple to result queue
            q.put((timestamp, temperature, humidity))

        time.sleep(sampleRate)
        

def save2file(outputFileHandler, flushing=True):
    ''' Write to fileHandler'''

if __name__ == "__main__":
    # Creating dataQueue and oledOnOffQueue
    dataQueue = multiprocessing.Queue()
    oledOnOffQueue = multiprocessing.Queue(maxsize=1)

    # Start process looking at button changes
    p1 = multiprocessing.Process(target=buttonGuard, args=(18, 0.01, oledOnOffQueue,))
    p1.start()

    # Start process reading data from DHT11
    p2 = multiprocessing.Process(target=readDHT, args=(22, 3, dataQueue))
    p2.start()
