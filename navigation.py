import time

import ultrasonic

import controls

WALL_DISTANCE_MAX = 100

FORWARD_DISTANCE = 300


def main() -> None:

    running = True

    while running:

        if not right_wall():
            controls.turn_right()
            controls.move_forward(FORWARD_DISTANCE)

        elif forward_wall() and right_wall():
            controls.turn_left()

        time.sleep(1)


def forward_wall() -> bool:
    return ultrasonic.forward_distance() <= WALL_DISTANCE_MAX


def right_wall() -> bool:
    return ultrasonic.right_distance() <= WALL_DISTANCE_MAX


if __name__ == "__main__":
    main()
