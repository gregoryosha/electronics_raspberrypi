import time
from multiprocessing import Manager, Process, Value

from flask import Flask, jsonify, render_template, request

from controls import *
import atexit

app = Flask(__name__)
# GPIO.setmode(GPIO.BOARD)

# GPIO.setup(40, GPIO.OUT)
# GPIO.setup(38, GPIO.OUT)

global_motor_states = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/printout")
def print_out():
    print("Successfuly get request!")
    return "success!"


@app.route("/digital/write/<pin_name>/<state_name>")
def digital_write(pin_name, state_name):
    pin = int(pin_name)
    if state_name == "HIGH":
        state = 1
    elif state_name == "LOW":
        state = 0
    if pin == 1:
        global_motor_states["forward"] = state
        global_motor_states["backward"] = 0
        global_motor_states["right"] = 0
        global_motor_states["left"] = 0
        return "forward"
    elif pin == 2:
        global_motor_states["forward"] = 0
        global_motor_states["backward"] = state
        global_motor_states["right"] = 0
        global_motor_states["left"] = 0
        return "backward"
    elif pin == 3:
        global_motor_states["forward"] = 0
        global_motor_states["backward"] = 0
        global_motor_states["right"] = state
        global_motor_states["left"] = 0
        return "right"
    elif pin == 4:
        global_motor_states["forward"] = 0
        global_motor_states["backward"] = 0
        global_motor_states["right"] = 0
        global_motor_states["left"] = state
        return "left"
    return "Something went wrong"


def record_loop(loop_on, global_motor_states):
    while True:
        if loop_on.value == True:
            if global_motor_states["forward"] == 1:
                print("moving forward")
                step(Direction.FORWARD)
            elif global_motor_states["backward"] == 1:
                print("moving backward")
                step(Direction.BACKWARD)
            elif global_motor_states["right"] == 1:
                print("turning right")
                rotate_right()
            elif global_motor_states["left"] == 1:
                print("turning left")
                rotate_left()

def exit_handler():
    GPIO.cleanup() 
    print ("exiting...")


if __name__ == "__main__":
    atexit.register(exit_handler)

    pin_setup()
    manager = Manager()
    motor_states = manager.dict()
    global_motor_states = motor_states
    motor_states["forward"] = 0
    motor_states["backward"] = 0
    motor_states["right"] = 0
    motor_states["left"] = 0
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
