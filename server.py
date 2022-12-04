from flask import Flask, render_template, jsonify, request
import time
from multiprocessing import Process, Value
import RPi.GPIO as GPIO

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)

pin_states = {
    40: GPIO.LOW,
    38: GPIO.LOW
}
GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)

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
        #GPIO.setup(pin, GPIO.OUT)   # pinMode(pin_name, OUTPUT)
        #GPIO.output(pin, GPIO.HIGH) # digitalWrite(pin_name, HIGH)
        pin_states[pin] = GPIO.HIGH
        return 'Set pin {0} to HIGH'.format(pin_name)
    elif state.upper() in ['0', 'OFF', 'LOW']:
        #GPIO.setup(pin, GPIO.OUT)   # pinMode(pin_name, OUTPUT)
        #GPIO.output(pin, GPIO.LOW)  # digitalWrite(pin_name, LOW)
        pin_states[pin] = GPIO.LOW
        return 'Set pin {0} to LOW'.format(pin_name)
    return 'Something went wrong'

def record_loop(loop_on):
   while True:
      if loop_on.value == True:
        print(pin_states[40])
        GPIO.output(40, pin_states[40])
        GPIO.output(38, pin_states[38])
      time.sleep(1)

if __name__ == "__main__":
   recording_on = Value('b', True)
   p = Process(target=record_loop, args=(recording_on,))
   p.start()  
   app.run(host='0.0.0.0', use_reloader=False, debug=True)
   p.join()
