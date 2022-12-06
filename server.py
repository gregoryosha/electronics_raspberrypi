from flask import Flask, render_template, jsonify, request
import time
from controls import *
from multiprocessing import Process, Manager, Value
import RPi.GPIO as GPIO

app = Flask(__name__)
#GPIO.setmode(GPIO.BOARD)

#GPIO.setup(40, GPIO.OUT)
#GPIO.setup(38, GPIO.OUT)

global_motor_states = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/printout')
def print_out():
    print('Successfuly get request!')
    return 'success!'

@app.route('/digital/write/<pin_name>/<state_name>')
def digital_write(pin_name, state_name):
    pin = int(pin_name)
    if(state_name == 'HIGH'):
        state = 1
    elif(state_name == 'LOW'):
        state = 0
    if (pin == 1):
        global_motor_states['forward'] = state
        global_motor_states['backward'] = 0
        global_motor_states['right'] = 0
        global_motor_states['left'] = 0
        return 'forward'
    elif(pin == 2):
        global_motor_states['forward'] = 0
        global_motor_states['backward'] = state
        global_motor_states['right'] = 0
        global_motor_states['left'] = 0
        return 'backward'
    elif(pin == 3):
        global_motor_states['forward'] = 0
        global_motor_states['backward'] = 0
        global_motor_states['right'] = state
        global_motor_states['left'] = 0
        return 'right'
    elif(pin == 4):
        global_motor_states['forward'] = 0
        global_motor_states['backward'] = 0
        global_motor_states['right'] = 0
        global_motor_states['left'] = state
        return 'left'
    # if state.upper() in ['1', 'ON', 'HIGH']:
    #     #GPIO.setup(pin, GPIO.OUT)   # pinMode(pin_name, OUTPUT)
    #     #GPIO.output(pin, GPIO.HIGH) # digitalWrite(pin_name, HIGH)
    #     return 'Set pin {0} to HIGH'.format(pin_name)
    # elif state.upper() in ['0', 'OFF', 'LOW']:
    #     #GPIO.setup(pin, GPIO.OUT)   # pinMode(pin_name, OUTPUT)
    #     #GPIO.output(pin, GPIO.LOW)  # digitalWrite(pin_name, LOW)
    #     global_motor_states[pin] = GPIO.LOW
    #     return 'Set pin {0} to LOW'.format(pin_name)
    return 'Something went wrong'

def record_loop(loop_on, global_motor_states):
    while True:
        if loop_on.value == True:
            if (global_motor_states['forward'] == 1):
                step_forward()
            elif (global_motor_states['backward'] == 1):
                step_backward()
            elif (global_motor_states['right'] == 1):
                rotate_right()
            elif (global_motor_states['left'] == 1):
                rotate_left()

if __name__ == "__main__":
    pin_setup()
    manager = Manager()
    motor_states = manager.dict()
    global_motor_states = motor_states
    motor_states['forward'] = 0
    motor_states['backward'] = 0
    motor_states['right'] = 0
    motor_states['left'] = 0
    recording_on = Value('b', True)
    p = Process(target=record_loop, args=(recording_on, motor_states,))
    p.start()  
    app.run(host='0.0.0.0', use_reloader=False, debug=True)
    p.join()
