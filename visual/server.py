#!flask/bin/python

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from api import State, util

from flask import Flask, render_template, request, redirect, Response
import random, json


app = Flask(__name__, template_folder='.')
app.config.update(
    PROPAGATE_EXCEPTIONS = True
)

state = None
player1 = util.load_player("rand")

@app.route('/')
def output():
	# serve index template
	# return "Welcome to python flask!"
	return render_template('index.html')

@app.route('/generate', methods = ['GET'])
def generate():
	global state
	state = State.generate()
	return state.convert_to_json()

@app.route('/next', methods = ['GET'])
def new():
	global state
	state = state.next(player1.get_move(state))
	return state.convert_to_json()



@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json(force=True)
	print data
	result = ''

	for item in data:
		# loop over every row
		result += str(item['make']) + '\n'

	return result

if __name__ == '__main__':
	# run!
	app.run(debug=True)