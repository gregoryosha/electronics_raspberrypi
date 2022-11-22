import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)   # use the BOARD pin-numbering system
GPIO.setup(16, GPIO.IN)       # like pinMode(16, INPUT)
while(1):                     # do this forever
    if(GPIO.input(16)):       # like digitalRead(16)
        print("Pin is high.")
    else:
        print("Pin is low.")
    time.sleep(0.5)           # sleep for 0.5 s