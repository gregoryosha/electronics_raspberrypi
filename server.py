from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

data = list(range(1,300,3))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/printout')
def print_out():
    print("Successfuly get request!")
    return 'success!'

@app.route('/digital/write/<pin_name>/<state>')
def digital_write(pin_name, state):
    pin = int(pin_name)
    if state.upper() in ['1', 'ON', 'HIGH']:
        GPIO.setup(pin, GPIO.OUT)   # pinMode(pin_name, OUTPUT)
        GPIO.output(pin, GPIO.HIGH) # digitalWrite(pin_name, HIGH)
        return 'Set pin {0} to HIGH'.format(pin_name)
    elif state.upper() in ['0', 'OFF', 'LOW']:
        GPIO.setup(pin, GPIO.OUT)   # pinMode(pin_name, OUTPUT)
        GPIO.output(pin, GPIO.LOW)  # digitalWrite(pin_name, LOW)
        return 'Set pin {0} to LOW'.format(pin_name)
    return 'Something went wrong'