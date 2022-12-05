import time
from enum import Enum, auto
from typing import Any

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

# CHANNEL = 7

GPIO.setmode(GPIO.BOARD)  # type: ignore
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

    # mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "Nema")

    # time.sleep(0.5)

    # # call the function pass the arguments
    # mymotortest.motor_run(MOTOR_LEFT_PINS, 0.01, 20, False, True, "half", 0.05)

    for pin in MOTOR_LEFT_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    halfstep_seq = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
    ]

    for i in range(300):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(MOTOR_LEFT_PINS[pin], halfstep_seq[halfstep][pin])
                time.sleep(0.01)

    GPIO.cleanup()  # type: ignore


if __name__ == "__main__":
    main()
