from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BOARD)

data = list(range(1,300,3))

@app.route('/')
def home():
    return render_template('index.html')

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


@app.route('/getdata/<index_no>', methods=['GET', 'POST'])
def data_get(index_no):

    if request.method == 'POST':    #POST request
        print(request.get_text())   #parse as text
        return 'OK', 200

    else: #GET request
        return 't_in = % ; result: %s ;'%(index_no, data[int(index_no)])