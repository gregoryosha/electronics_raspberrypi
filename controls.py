import math
import time
from enum import Enum, auto
from typing import Any, Literal

import RPi.GPIO as GPIO

CLOCKWISE = True
COUNTER_CLOCKWISE = False

FORWARD = (CLOCKWISE, COUNTER_CLOCKWISE)
BACKWARD = (COUNTER_CLOCKWISE, CLOCKWISE)

STEPS_PER_ROTATION = 50

RADIUS_WHEEL_MM = 45

TURNING_RADIUS_MM = 85

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

    turn_rotation(3, 5, FORWARD)

    time.sleep(1)

    turn_rotation(1, 3, BACKWARD)

    GPIO.cleanup()  # type: ignore


def turn(degrees, time_seconds, turn_direction):

    directions = (
        (COUNTER_CLOCKWISE, COUNTER_CLOCKWISE)
        if turn_direction == CLOCKWISE
        else (CLOCKWISE, CLOCKWISE)
    )

    distance_mm = 2 * math.pi * TURNING_RADIUS_MM * degrees / 360

    move_distance(distance_mm, time_seconds, directions)


def move_distance(distance_mm, time_seconds, directions: tuple[bool, bool] = FORWARD):
    # Calculates circumference of wheel
    circumference = 2 * math.pi * RADIUS_WHEEL_MM
    # Turns number of rotations needed to move distance
    turn_rotation(distance_mm / circumference, time_seconds)


def turn_rotation(
    number_rotations: float,
    time_seconds: float,
    directions: tuple[bool, bool] = FORWARD,
) -> None:
    """Moves specified motors a number of rotations in an amount of time in a direction."""
    # Defines a halfstep sequence

    if number_rotations > time_seconds:
        raise ValueError("Too many rotations! Use a larger time!")

    sequences = []

    for direction in directions:
        if direction == CLOCKWISE:
            sequences.append(HALFSTEP_SEQUENCE)
        else:
            sequences.append(HALFSTEP_SEQUENCE[::-1])

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
                # Accesses exact pin values from each corresponding sequence
                GPIO.output(MOTOR_LEFT_PINS[pin], sequences[0][halfstep][pin])  # type: ignore
                GPIO.output(MOTOR_RIGHT_PINS[pin], sequences[1][halfstep][pin])  # type: ignore
                time.sleep(delay)


if __name__ == "__main__":
    main()
