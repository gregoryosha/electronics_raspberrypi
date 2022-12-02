import time
from enum import Enum, auto
from typing import Any

import RPi.GPIO as GPIO
import RpiMotorLib as stepper

CHANNEL = 7

GPIO.setmode(GPIO.BOARD)  # type: ignore
GPIO.setup(CHANNEL, GPIO.OUT)  # type: ignore

MOTOR_A_PINS = list(range(27, 35, 2))
MOTOR_B_PINS = list(range(35, 39))


# direction = 20  # Direction -> GPIO Pin
# step = 21  # Step -> GPIO Pin

# # Declare a instance of class pass GPIO pins numbers and the motor type
# mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "DRV8825")

# # call the function, pass the arguments
# mymotortest.motor_go(False, "Full", 100, 0.01, False, 0.05)


def main():
    for i in range(5):
        time.sleep(1)
        GPIO.output(CHANNEL, True)  # type: ignore
        time.sleep(1)
        GPIO.output(CHANNEL, False)  # type: ignore


if __name__ == "__main__":
    main()
