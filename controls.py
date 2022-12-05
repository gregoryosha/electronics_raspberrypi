import math
import time
from enum import Enum
from typing import Any

import RPi.GPIO as GPIO

CLOCKWISE = 1
COUNTER_CLOCKWISE = -1


class Direction(Enum):
    FORWARD = (COUNTER_CLOCKWISE, CLOCKWISE)
    BACKWARD = (CLOCKWISE, COUNTER_CLOCKWISE)
    LEFT = (CLOCKWISE, CLOCKWISE)
    RIGHT = (COUNTER_CLOCKWISE, COUNTER_CLOCKWISE)


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

# MOTOR_LEFT_PINS = [11, 13, 15, 16]
MOTOR_LEFT_PINS = [15, 11, 13, 16]
# MOTOR_RIGHT_PINS = [29, 31, 32, 33]
MOTOR_RIGHT_PINS = [31, 29, 32, 33]


def main() -> None:
    """Runs main actions for testing sequence."""
    # Sets board mode
    GPIO.setmode(GPIO.BOARD)  # type: ignore
    # Sets all motor pins to output and disengages them
    for pin in MOTOR_LEFT_PINS + MOTOR_RIGHT_PINS:
        GPIO.setup(pin, GPIO.OUT)  # type: ignore
        GPIO.output(pin, False)  # type: ignore

    _engage_motors(1, 1)

    time.sleep(1)

    _engage_motors(3, 5, Direction.FORWARD)

    time.sleep(1)

    _engage_motors(1, 3, Direction.BACKWARD)

    # Turns off any pins left on
    GPIO.cleanup()  # type: ignore


def rotate_degrees(
    degrees: float, time_seconds: float, turn_direction: Direction
) -> None:
    """Turns robot specified degrees in an amount of time in a direction."""

    # Calculates perimeter distance needed to travel
    distance_mm = 2 * math.pi * TURNING_RADIUS_MM * degrees / 360
    # Moves calculated distance
    move_distance(distance_mm, time_seconds, turn_direction)


def move_distance(
    distance_mm: float, time_seconds: float, direction: Direction = Direction.FORWARD
) -> None:
    """Turns motors a GROUND DISTANCE in an amount of time in a direction."""

    # Calculates circumference of wheel
    circumference = 2 * math.pi * RADIUS_WHEEL_MM
    # Turns number of rotations needed to move distance
    _engage_motors((distance_mm / circumference), time_seconds, direction)


def _engage_motors(
    number_rotations: float,
    time_seconds: float,
    direction: Direction = Direction.FORWARD,
) -> None:
    """Turns motors a NUMBER OF ROTATIONS in an amount of time in a direction."""

    # Throws error if motor would be turning too fast
    if number_rotations > time_seconds:
        raise ValueError("Too many rotations! Use a larger time!")

    # Defines a number of steps
    steps_count = int(STEPS_PER_ROTATION * number_rotations)
    # Defines a number of halfsteps in sequence
    halfsteps_count = len(HALFSTEP_SEQUENCE)
    # Defines the number of pins used in sequence
    pins_count = len(HALFSTEP_SEQUENCE[0])

    # Calculates a delay between pin activations
    delay = time_seconds / (steps_count * halfsteps_count * pins_count)

    # For as many steps as specified:
    for _ in range(steps_count):
        # For each halfstep in sequence
        for halfstep in range(halfsteps_count):
            # For each pin value
            for pin in range(pins_count):
                # Assigns corresponding motor pins to sequence in specified direction
                GPIO.output(MOTOR_LEFT_PINS[pin], HALFSTEP_SEQUENCE[:: direction.value[0]][halfstep][pin])  # type: ignore
                GPIO.output(MOTOR_RIGHT_PINS[pin], HALFSTEP_SEQUENCE[:: direction.value[1]][halfstep][pin])  # type: ignore
                # Sleeps for calculated delay
                time.sleep(delay)


# ======== DEFAULT FUNCTIONS ======== #


def move_forward(distance_mm: float = 200, time_seconds: float = 3):
    """Moves robot forward. Optional: Distance, Time."""
    move_distance(distance_mm, time_seconds, Direction.FORWARD)


def move_backward(distance_mm: float = 200, time_seconds: float = 3):
    """Moves robot forward. Optional: Distance, Time."""
    move_distance(distance_mm, time_seconds, Direction.BACKWARD)


def rotate_left(degrees: float = 90, time_seconds: float = 2) -> None:
    """Rotates robot to the left. Optional: Degrees, Time."""
    rotate_degrees(degrees, time_seconds, Direction.LEFT)


def rotate_right(degrees: float = 90, time_seconds: float = 2) -> None:
    """Rotates robot to the right. Optional: Degrees, Time."""
    rotate_degrees(degrees, time_seconds, Direction.RIGHT)


# Runs main only from command line call instead of library call
if __name__ == "__main__":
    main()
