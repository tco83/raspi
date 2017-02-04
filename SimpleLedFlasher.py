import time
import random
import RPi.GPIO as GPIO

# Adressierung der PINs definieren
GPIO.setmode(GPIO.BOARD)

# Pin11 als Output definieren
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

starttime = time.time()
currenttime = time.time()
x=0.15

# Schleife für 7 Sekunden
while currenttime - starttime < 10:
    # LED an
    GPIO.output(15, GPIO.LOW)
    GPIO.output(11, GPIO.HIGH)

    time.sleep(x)

    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.HIGH)

    time.sleep(x)

    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.HIGH)

    time.sleep(x)
    
    currenttime = time.time()

print('Geschafft. Laufzeit: '+str(round(currenttime-starttime,1))+' Sekunden')
    
# Vorherige PIN-Mappings entfernen
GPIO.cleanup()
