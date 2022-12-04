from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

pin_states = {
    40: GPIO.LOW,
    38: GPIO.LOW
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/printout')
def print_out():
    print('Successfuly get request!')
    return 'success!'

@app.route('/digital/write/<pin_name>/<state>')
def digital_write(pin_name, state):
    pin = int(pin_name)
    if state.upper() in ['1', 'ON', 'HIGH']:
        GPIO.setup(pin, GPIO.OUT)   # pinMode(pin_name, OUTPUT)
        #GPIO.output(pin, GPIO.HIGH) # digitalWrite(pin_name, HIGH)
        pin_states[pin] = GPIO.HIGH
        return 'Set pin {0} to HIGH'.format(pin_name)
    elif state.upper() in ['0', 'OFF', 'LOW']:
        GPIO.setup(pin, GPIO.OUT)   # pinMode(pin_name, OUTPUT)
        #GPIO.output(pin, GPIO.LOW)  # digitalWrite(pin_name, LOW)
        pin_states[pin] = GPIO.LOW
        return 'Set pin {0} to LOW'.format(pin_name)
    return 'Something went wrong'

async def control_loop():
    while True:
        print("looping")
        GPIO.output(40, pin_states[40])
        GPIO.output(38, pin_states[38])

control_loop()
app.run(host='0.0.0.0', use_reloader=False, debug=True)
