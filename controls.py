import math
import time
from enum import Enum, auto
from typing import Any

import RPi.GPIO as GPIO

CLOCKWISE = True
COUNTER_CLOCKWISE = False

STEPS_PER_ROTATION = 50

RADIUS_WHEEL_MM = 45

HALFSTEP_SEQUENCE = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]


class Direction(Enum):
    Clockwise = True
    CounterClockwise = False


# MM_PER_ROTATION = 282.74

# CHANNEL = 7

GPIO.setmode(GPIO.BOARD)  # type: ignore
# GPIO.setup(CHANNEL, GPIO.OUT)  # type: ignore


# MOTOR_LEFT_PINS = [11, 13, 15, 16]
MOTOR_LEFT_PINS = [15, 11, 13, 16]
# MOTOR_RIGHT_PINS = [29, 31, 32, 33]
MOTOR_RIGHT_PINS = [31, 29, 32, 33]


def main():

    for pin in MOTOR_LEFT_PINS + MOTOR_RIGHT_PINS:
        GPIO.setup(pin, GPIO.OUT)  # type: ignore
        GPIO.output(pin, 0)  # type: ignore

    turn_rotation(1, 1)

    time.sleep(1)

    turn_rotation(3, 5, [COUNTER_CLOCKWISE, COUNTER_CLOCKWISE])

    time.sleep(1)

    turn_rotation(1, 3, [CLOCKWISE, COUNTER_CLOCKWISE])

    GPIO.cleanup()  # type: ignore


def move_distance(distance_mm, time_seconds, directions: bool = True):
    # Calculates circumference of wheel
    circumference = 2 * math.pi * RADIUS_WHEEL_MM
    # Turns number of rotations needed to move distance
    turn_rotation(distance_mm / circumference, time_seconds)


def turn_rotation(
    number_rotations: float,
    time_seconds: float,
    directions: list[bool] = [CLOCKWISE, CLOCKWISE],
) -> None:
    """Moves specified motors a number of rotations in an amount of time in a direction."""
    # Defines a halfstep sequence
    sequences = []

    for direction in directions:
        if direction == CLOCKWISE:
            sequences.append(HALFSTEP_SEQUENCE)
        else:
            sequences.append(HALFSTEP_SEQUENCE.reverse())

    # Defines a number of steps
    num_steps = int(STEPS_PER_ROTATION * number_rotations)

    num_halfsteps = len(HALFSTEP_SEQUENCE)

    num_pins = len(HALFSTEP_SEQUENCE[0])

    delay = time_seconds / (num_steps * num_halfsteps * num_pins)

    # For as many steps as specified:
    for _ in range(num_steps):
        # For each halfstep in sequence
        for halfstep in range(num_halfsteps):
            # For each pin value
            for pin in range(num_pins):
                GPIO.output(MOTOR_LEFT_PINS[pin], sequences[0][halfstep][pin])  # type: ignore
                GPIO.output(MOTOR_RIGHT_PINS[pin], sequences[1][halfstep][pin])  # type: ignore
                time.sleep(delay)


if __name__ == "__main__":
    main()
