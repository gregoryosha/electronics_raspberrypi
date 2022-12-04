import time
from enum import Enum, auto
from typing import Any

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

# CHANNEL = 7

# GPIO.setmode(GPIO.BOARD)  # type: ignore
# GPIO.setup(CHANNEL, GPIO.OUT)  # type: ignore

MOTOR_LEFT_PINS = [11, 13, 15, 16]
MOTOR_RIGHT_PINS = [29, 31, 32, 33]


def main():
    # for i in range(5):
    #     time.sleep(1)
    #     GPIO.output(CHANNEL, True)  # type: ignore
    #     time.sleep(1)
    #     GPIO.output(CHANNEL, False)  # type: ignore

    # Declare an named instance of class pass a name and type of motor

    mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "Nema")

    time.sleep(0.5)

    # call the function pass the arguments
    mymotortest.motor_run(MOTOR_LEFT_PINS, 0.01, 20, False, True, "half", 0.05)

    GPIO.cleanup()  # type: ignore


if __name__ == "__main__":
    main()
