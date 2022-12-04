import RPi.GPIO as GPIO

CHANNEL = 29

GPIO.setmode(GPIO.BOARD)  # type: ignore
GPIO.setup(CHANNEL, GPIO.OUT)  # type: ignore
