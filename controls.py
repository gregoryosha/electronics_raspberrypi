import math
import time
from enum import Enum, auto
from typing import Any

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

STEPS_PER_ROTATION = 50

RADIUS_WHEEL_MM = 45

# MM_PER_ROTATION = 282.74

# CHANNEL = 7

GPIO.setmode(GPIO.BOARD)  # type: ignore
# GPIO.setup(CHANNEL, GPIO.OUT)  # type: ignore


# 3 1 2 4

# 1 Y
# 2 G
# 3 R
# 4 B

# CURR ORDER: R, Y, G, B

# MOTOR_LEFT_PINS = [15, 11, 13, 16]
MOTOR_LEFT_PINS = [11, 13, 15, 16]
# MOTOR_RIGHT_PINS = [29, 31, 32, 33]
MOTOR_RIGHT_PINS = [32, 29, 31, 33]


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

    for pin in MOTOR_LEFT_PINS + MOTOR_RIGHT_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    turn_rotation(1, 1)

    time.sleep(1)

    turn_rotation(3, 5, False)

    time.sleep(1)

    turn_rotation(1, 3)

    GPIO.cleanup()  # type: ignore


def move_distance(distance_mm, time_seconds, clockwise: bool = True):
    # Calculates circumference of wheel
    circumference = 2 * math.pi * RADIUS_WHEEL_MM
    # Turns number of rotations needed to move distance
    turn_rotation(distance_mm / circumference, time_seconds, clockwise)


def turn_rotation(
    number_rotations: float, time_seconds: float, clockwise: bool = True
) -> None:
    """Moves specified motors a number of rotations in an amount of time in a direction."""
    # Defines a halfstep sequence
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
    # Reverses if not clockwise
    if not clockwise:
        halfstep_seq.reverse()
    # Defines a number of steps
    num_steps = int(STEPS_PER_ROTATION * number_rotations)

    num_halfsteps = len(halfstep_seq)

    num_pins = len(halfstep_seq[0])

    delay = time_seconds / (num_steps * num_halfsteps * num_pins)

    for i in range(num_steps):
        for halfstep in range(num_halfsteps):
            for pin in range(num_pins):
                GPIO.output(MOTOR_LEFT_PINS[pin], halfstep_seq[halfstep][pin])
                GPIO.output(MOTOR_RIGHT_PINS[pin], halfstep_seq[halfstep][pin])
                time.sleep(delay)


if __name__ == "__main__":
    main()
