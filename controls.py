import time
from enum import Enum, auto
from typing import Any

import RPi.GPIO as GPIO

CHANNEL = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(CHANNEL, GPIO.OUT)

while True:
    time.sleep(1)
    GPIO.output(CHANNEL, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(CHANNEL, GPIO.LOW)
