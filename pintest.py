import RPi.GPIO as GPIO

import controls

# controls.rotate_left()

CHANNEL = 29

GPIO.setmode(GPIO.BOARD)  # type: ignore
GPIO.setup(CHANNEL, GPIO.OUT)  # type: ignore