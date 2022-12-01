from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

@app.route('/')
def home():
    example_embed='This string is from python'
    return render_template('index.html', embed=example_embed)