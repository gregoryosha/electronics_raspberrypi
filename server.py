from flask import Flask
app = Flask(__name__)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pinon')
def pin_on():
    GPIO.setup(16, GPIO.OUT)   # pinMode(16, OUTPUT)
    GPIO.output(16, GPIO.HIGH) # digitalWrite(16, HIGH)
    return 'I turned on the pin.'

# Below we take input from a web browser and channel it to GPIO pin.
# app.route refers to your Pi's IP address, which you'll type into a web browser URL line when you want to control this code.
# For example, to set pin 16 on your Pi to HIGH, in your web browser you'll type [your Pi IP address]/digital/write/16/HIGH.
# Make sure the line below has the correct angle brackets in it.
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