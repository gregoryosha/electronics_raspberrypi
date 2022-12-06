import time

import RPi.GPIO as GPIO

import controls

time.sleep(1)

controls.move_forward(1168)

time.sleep(1)

controls.rotate_right()

time.sleep(1)

controls.move_forward(300)

time.sleep(1)

GPIO.cleanup()  # type: ignore
