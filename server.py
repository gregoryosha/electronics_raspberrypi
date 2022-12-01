from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

@app.route('/')
def home():
    example_embed='This string is from python'
    return render_template('index.html', embed=example_embed)

@app.route('/test', methods=['GET', 'POST'])
def test_function():

    #GET request
    if request.method == 'GET':
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message) #Use JSON headers and serialize
    
    #POST request
    if request.method == 'POST':
        print(request.get_json()) #Parse as JSON
        return 'Sucess', 200