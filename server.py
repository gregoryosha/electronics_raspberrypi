#!/usr/bin/env python
"""
Provides server interactivity with motor controls. Communicates with running 
server to execute controls commands via `Flask`.
"""

import atexit
import time
from multiprocessing import Manager, Process, Value
from typing import NoReturn

from flask import Flask, render_template, Response

import cv2

import controls
from controls import Direction

__author__ = "Greg Osha"
__copyright__ = "None"
__credits__ = ["Greg Osha", "Ben Kraft"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "N/A"
__email__ = "N/A"
__status__ = "Prototype"

DIRECTIONS = (Direction.FORWARD, Direction.BACKWARD, Direction.LEFT, Direction.RIGHT)

app = Flask(__name__)
camera = cv2.VideoCapture(0) #creates a local camera

global_motor_states = {}


def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/digital/write/<direction_id>/<value>")
def digital_write(direction_id: str, value: str) -> str:
    """Allows for flask writing of states."""

    # Assigns corrected direction index
    direction_index = int(direction_id) - 1
    # Throws error for invalid direction ID
    if direction_index not in range(len(DIRECTIONS)):
        raise ValueError("Inappropriate direction id, use between 1 and 4.")

    # Defines value names
    VALUE_NAMES = ("LOW", "HIGH")
    # Throws error for invalid value
    if value not in VALUE_NAMES:
        raise ValueError("Inappropriate value, use 'LOW' or 'HIGH'.")
    # Converts value to integer
    int_value = VALUE_NAMES.index(value)

    # For every direction:
    for i, direction in enumerate(DIRECTIONS):
        # Set dictionary value of specified direction to value, and all others to 0
        global_motor_states[direction] = int_value if i == direction_index else 0
    # Return the specified direction name
    return DIRECTIONS[direction_index].name


def record_loop(loop_on, global_motor_states: dict[Direction, int]) -> NoReturn:
    while True:
        if loop_on.value:
            if global_motor_states[Direction.FORWARD]:
                print("Moving forward...")
                controls.step(Direction.FORWARD)
            elif global_motor_states[Direction.BACKWARD]:
                print("Moving backward...")
                controls.step(Direction.BACKWARD)
            elif global_motor_states[Direction.RIGHT]:
                print("Turning right...")
                controls.turn_degrees(15, 1, Direction.RIGHT)
            elif global_motor_states[Direction.LEFT]:
                print("Turning left...")
                controls.turn_degrees(15, 1, Direction.LEFT)


def exit_handler() -> None:
    # Cleans up GPIO pins
    controls.cleanup()
    print("Exiting...")


if __name__ == "__main__":
    atexit.register(exit_handler)

    controls.pin_setup()
    manager = Manager()
    motor_states = manager.dict()
    global_motor_states = motor_states

    for direction in DIRECTIONS:
        motor_states[direction] = 0

    recording_on = Value("b", True)
    p = Process(
        target=record_loop,
        args=(
            recording_on,
            motor_states,
        ),
    )
    p.start()
    app.run(host="0.0.0.0", use_reloader=False, debug=True)
    p.join()
