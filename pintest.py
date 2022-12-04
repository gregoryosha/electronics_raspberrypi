import RPi.GPIO as GPIO

CHANNEL = 27

GPIO.setmode(GPIO.BOARD)  # type: ignore
GPIO.setup(CHANNEL, GPIO.OUT)  # type: ignore
