import time
from enum import Enum, auto
from typing import Any

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

STEPS_PER_ROTATION = 50

# CHANNEL = 7

GPIO.setmode(GPIO.BOARD)  # type: ignore
# GPIO.setup(CHANNEL, GPIO.OUT)  # type: ignore

MOTOR_LEFT_PINS = [15, 11, 13, 16]
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

    turn_rotation(1, 1)

    time.sleep(1)

    turn_rotation(3, 5)

    time.sleep(1)

    turn_rotation(1, 3)

    GPIO.cleanup()  # type: ignore


def turn_rotation(number_rotations: float, time_seconds: float) -> None:

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

    num_steps = int(STEPS_PER_ROTATION * number_rotations)

    num_halfsteps = len(halfstep_seq)

    num_pins = len(halfstep_seq[0])

    delay = time_seconds / (num_steps * num_halfsteps * num_pins)

    for i in range(num_steps):
        for halfstep in range(num_halfsteps):
            for pin in range(num_pins):
                GPIO.output(MOTOR_LEFT_PINS[pin], halfstep_seq[halfstep][pin])
                time.sleep(delay)


if __name__ == "__main__":
    main()
