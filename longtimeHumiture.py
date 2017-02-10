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
    
def buttonGuard(q, pin=18, sampleRate=0.01):
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
                # uncomment following line if you want to see if your button press worked
                #print("Pushbutton -> queueing done!")
            elif buttonPressed == True and q.full():
                pass
                # uncomment following line if needed for debugging
                #print("Pushbutton -> queue still unread!")

            buttonPressed = False
            
        time.sleep(sampleRate)

def readDHT(q, pin=22, sampleRate=2):
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

            # uncomment following line for debbuging purposes
            #print("%s || %dC %d%%" % (timestamp, temperature, humidity))

        time.sleep(sampleRate)
        

def save2file(outputFileHandler, data, flushing=True):
    ''' Write to fileHandler'''
    outputElements = []

    # create list of String Elements from data tuple or list
    for element in data:
        if type(element) != str:
            outputElements.append(str(element))
        else:
            outputElements.append(element)

    # join output data together in CSV data format
    outputStr = ";".join(outputElements)
    outputStr += "\n"

    outputFileHandler.write(outputStr)
    if flushing == True:
        outputFileHandler.flush()

def initDisplay(font, showTime=2):
    with canvas(device) as draw:
        draw.text((0,0), "IN", font=font, fill="white")
        draw.text((0,32), "IT", font=font, fill="white")
        time.sleep(showTime)
        draw.rectangle((0,0,device.width, device.height), fill="black")
        

def writeOnDisplay(t, h, font):
    with canvas(device) as draw:
        draw.text((0,0), "%dC" % t, font=font, fill="white")
        draw.text((0,32), "%d%%" % h, font=font, fill="white")
        #draw.text((0,0), "test", font=font, fill="white")

def clearDisplay():
    with canvas(device) as draw:
        draw.rectangle((0,0,device.width, device.height), fill="black")

def createFontHandler(fontName="fonts/upheavtt.ttf", fontSize=40):
    return ImageFont.truetype(fontName, fontSize)

if __name__ == "__main__":
    # Initialize GPIO
    initGPIO()

    # Initialize oled
    oledOn = False
    
    # Creating dataQueue and oledOnOffQueue
    dataQueue = multiprocessing.Queue()
    oledOnOffQueue = multiprocessing.Queue(maxsize=1)

    # Start process looking at button changes
    p1 = multiprocessing.Process(target=buttonGuard, args=(oledOnOffQueue, 18, 0.025, ))
    p1.start()

    # Start process reading data from DHT11
    p2 = multiprocessing.Process(target=readDHT, args=(dataQueue, 22, 5, ))
    p2.start()

    # Initialize everything for the OLED display
    fontHandler = createFontHandler()
    try:
        # create outputFileHandler relative to timestamp - prevent overwrite on multiple runs
        oFile = "output/out_%d.csv" % round(time.time())
        oH = open(oFile, mode="a")

        # initialize Display for 2 seconds to give the DHT a headstart with data
        # and show that the display actually works
        initDisplay(fontHandler, showTime=2)
        
        while True:
            # Check if there's new data in dataQueue
            if not dataQueue.empty():
                # get latest Results from result Queue - and preserve for OLED display
                lastResult = dataQueue.get()
                save2file(oH, lastResult)

            # Check if button was pressed, changing oledOn flag
            if not oledOnOffQueue.empty():
                val = oledOnOffQueue.get()
                if oledOn == False and val == True:
                    oledOn = True
                elif oledOn == True and val == True:
                    oledOn = False

            # If display is to be on, write last value to display
            if oledOn == True:
                t = lastResult[1]
                h = lastResult[2]
                writeOnDisplay(t, h, fontHandler)
            elif oledOn == False:
                clearDisplay()
                
        time.sleep(1)                
                
    except KeyboardInterrupt:
        print("")
        print("===================")
        print("=== TERMINATING ===")
        print("===================")
        # Terminating processes
        p1.terminate()
        p2.terminate()
        print("Processes terminated")

        # Closing file handlers
        oH.close()
        print("output file handlers closed")
        
        # Clearing Display
        clearDisplay()
        print("Display cleared")
    
