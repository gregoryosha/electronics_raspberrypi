import time
from enum import Enum, auto
from typing import Any

import RPi.GPIO as GPIO

CHANNEL = 7

GPIO.setmode(GPIO.BOARD)  # type: ignore
GPIO.setup(CHANNEL, GPIO.OUT)  # type: ignore

while True:
    time.sleep(1)
    GPIO.output(CHANNEL, True)  # type: ignore
    time.sleep(1)
    GPIO.output(CHANNEL, False)  # type: ignore
