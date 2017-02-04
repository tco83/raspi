import RPi.GPIO as GPIO
import time

# Adressierungs-Schema der PINs festlegen
GPIO.setmode(GPIO.BOARD)

# PIN 12 als Input-PIN mit Default True (PUD_UP) definieren.
# der Druck des Buttons zieht dann runter (False)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Timer Variablen initialisieren
starttime = 0
endtime = 0

while True:
    input_state = GPIO.input(12)

    if input_state == False:
        if starttime == 0:
            starttime = time.time()

        endtime = time.time()
        time.sleep(0.01)

    if input_state == True:
        if starttime != 0 and endtime != 0:
            print('Button was pressed for ' + str(round(endtime-starttime,3)) + ' seconds.')
            # Reset für den nächsten Durchlauf
            starttime = 0
            endtime = 0
        time.sleep(0.01)
