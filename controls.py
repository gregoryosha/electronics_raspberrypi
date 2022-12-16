#!/usr/bin/env python
"""
Provides control for a dual-stepper-motor setup. Allows for two-directional 
movement and rotation at varying speeds. Allows for use of `move_forward()`, 
`move_backward()`, `turn_left()`, `turn_right()`, as well as other helpful 
functions.
"""

import math
import time
from enum import Enum

import RPi.GPIO as GPIO

__author__ = "Ben Kraft"
__copyright__ = "None"
__credits__ = "Ben Kraft"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Ben Kraft"
__email__ = "benjamin.kraft@tufts.edu"
__status__ = "Prototype"

# Defines motor spins
CLOCKWISE = -1
COUNTER_CLOCKWISE = 1

# Enum for directions
class Direction(Enum):
    FORWARD = (COUNTER_CLOCKWISE, COUNTER_CLOCKWISE)
    BACKWARD = (CLOCKWISE, CLOCKWISE)
    LEFT = (CLOCKWISE, COUNTER_CLOCKWISE)
    RIGHT = (COUNTER_CLOCKWISE, CLOCKWISE)


# Reference lists
TRANSLATIONAL_DIRECTIONS = (Direction.FORWARD, Direction.BACKWARD)
ROTATIONAL_DIRECTIONS = (Direction.LEFT, Direction.RIGHT)

# Refered constants
STEPS_PER_ROTATION = 50
MINIMUM_MOTOR_DELAY = 0.001

RADIUS_WHEEL_MM = 45
WHEEL_CIRCUMFERENCE = 2 * math.pi * RADIUS_WHEEL_MM

TURNING_RADIUS_MM = 88
TURNING_CIRCUMFERENCE = 2 * math.pi * TURNING_RADIUS_MM

# Half-step stepper motor sequence
HALFSTEP_SEQUENCE = (
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1),
)
# Defines a number of halfsteps in sequence
HALFSTEPS_COUNT = len(HALFSTEP_SEQUENCE)
# Defines the number of pins used in sequence
HALFSTEP_PINS_COUNT = len(HALFSTEP_SEQUENCE[0])

# MOTOR_LEFT_PINS = (11, 13, 15, 16)
MOTOR_LEFT_PINS = (15, 11, 13, 16)
# MOTOR_RIGHT_PINS = (29, 31, 32, 33)
MOTOR_RIGHT_PINS = (31, 29, 32, 33)


def main() -> None:
    """Runs actions for testing sequence."""
    pin_setup()

    move_forward()
    time.sleep(1)
    move_backward(200, 1)
    time.sleep(1)
    turn_left()
    time.sleep(1)
    turn_right()

    pin_cleanup()


def pin_setup() -> None:
    """
    Sets up board mode and motor pins.
    """
    # Sets board mode
    GPIO.setmode(GPIO.BOARD)  # type: ignore
    # Sets all motor pins to output and disengages them
    for pin in MOTOR_LEFT_PINS + MOTOR_RIGHT_PINS:
        GPIO.setup(pin, GPIO.OUT)  # type: ignore
        GPIO.output(pin, False)  # type: ignore


def pin_cleanup() -> None:
    """
    Turns off any pins left on.
    """
    GPIO.cleanup()  # type: ignore


def turn_degrees(degrees: float, time_seconds: float, direction: Direction) -> None:
    """
    Turns robot specified degrees in an amount of time in a direction.
    """
    # Raises error if not in rotational directions
    if direction not in ROTATIONAL_DIRECTIONS:
        raise ValueError("Invalid direction for rotational movement.")

    # Calculates perimeter distance needed to travel
    distance_mm = TURNING_CIRCUMFERENCE * degrees / 360
    # Moves calculated distance
    _rotate_motors((distance_mm / WHEEL_CIRCUMFERENCE), time_seconds, direction)


def move_distance(
    distance_mm: float, time_seconds: float, direction: Direction = Direction.FORWARD
) -> None:
    """
    Turns motors a ground distance in an amount of time in a direction.
    """
    # Raises error if not in translational directions
    if direction not in TRANSLATIONAL_DIRECTIONS:
        raise ValueError("Invalid direction for translational movement.")

    # Turns number of rotations needed to move distance
    _rotate_motors((distance_mm / WHEEL_CIRCUMFERENCE), time_seconds, direction)


def _rotate_motors(
    number_rotations: float, time_seconds: float, direction: Direction
) -> None:
    """
    Turns motors a number of rotations in an amount of time in a direction.
    """
    # Defines a number of steps
    steps_count = int(STEPS_PER_ROTATION * number_rotations)

    # Calculates a delay between pin activations
    delay = time_seconds / steps_count / HALFSTEPS_COUNT / HALFSTEP_PINS_COUNT

    # For as many steps as specified:
    for _ in range(steps_count):
        # Move one step in direction
        _step_motors(direction, delay)


def _step_motors(direction: Direction, delay: float = MINIMUM_MOTOR_DELAY) -> None:
    """
    Moves motors one step in direction. Optional: Step delay.
    """
    # Throws error if moving to quickly
    if delay < MINIMUM_MOTOR_DELAY:
        raise ValueError("Too fast to turn! Use a larger time!")

    # Defines the sequence for each motor from specified direction
    sequences = tuple(HALFSTEP_SEQUENCE[::i] for i in direction.value)
    # For each halfstep in sequence
    for halfstep in range(HALFSTEPS_COUNT):
        # For each pin value
        for pin in range(HALFSTEP_PINS_COUNT):
            # Assigns corresponding motor pins to action from designated sequence
            GPIO.output(MOTOR_LEFT_PINS[pin], sequences[0][halfstep][pin])  # type: ignore
            GPIO.output(MOTOR_RIGHT_PINS[pin], sequences[1][halfstep][pin])  # type: ignore
            # THIS TIMER WORKS BUT SHOULD IN BE WITHIN THIS LOOP OR THE ONE
            # BELOW, BECAUSE DO THE PINS NEED TIME BETWEEN EACH ONE ACTIVATING
            # OR JUST EACH HALFSTEP STAGE??? I'M SCARED TO TRY IT .･(>д<)･. -BK
            time.sleep(delay)


# ======== DEFAULT FUNCTIONS ======== #


def step(direction: Direction = Direction.FORWARD):
    """
    Steps motors forward in specified direction.
    """
    _step_motors(direction)


def move_forward(distance_mm: float = 250, time_seconds: float = 3) -> None:
    """
    Moves robot forward. Optional: Distance, Time.
    """
    move_distance(distance_mm, time_seconds, Direction.FORWARD)


def move_backward(distance_mm: float = 250, time_seconds: float = 3) -> None:
    """
    Moves robot forward. Optional: Distance, Time.
    """
    move_distance(distance_mm, time_seconds, Direction.BACKWARD)


def turn_left(degrees: float = 90, time_seconds: float = 2) -> None:
    """
    Rotates robot to the left. Optional: Degrees, Time.
    """
    turn_degrees(degrees, time_seconds, Direction.LEFT)


def turn_right(degrees: float = 90, time_seconds: float = 2) -> None:
    """
    Rotates robot to the right. Optional: Degrees, Time.
    """
    turn_degrees(degrees, time_seconds, Direction.RIGHT)


# Runs main only from command line call instead of library call
if __name__ == "__main__":
    main()
