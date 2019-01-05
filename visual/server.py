#!flask/bin/python

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from api import State, util
from argparse import ArgumentParser
import random
import json


from flask import Flask, render_template, request, redirect, Response
import random, json


app = Flask(__name__, template_folder='.')
app.config.update(
	PROPAGATE_EXCEPTIONS = True
)



@app.route('/')
def output():
	# serve index template
	# return "Welcome to python flask!"
	temp = "index_interactive.html" if options.interactive else "index.html"
	return render_template(temp)

@app.route('/generate', methods = ['GET'])
def generate():
	global state
	# Use 3 for marriage, 50 for exchange
	state = State.generate()
	return state.convert_to_json() #[:-1] + ', "seed": ' + str(id) + '}')

@app.route('/next', methods = ['GET'])
def new():
	global state

	player = player1 if (state.whose_turn() == 1 and not options.interactive) else player2

	given_state = state.clone(signature=state.whose_turn()) if state.get_phase() == 1 else state.clone()

	state = state.next(player.get_move(given_state))
	return state.convert_to_json()

@app.route('/sendmove', methods = ['POST'])
def send():
	global state
	data = request.get_json(force=True)
	move = (data[0], data[1])
	state = state.next(move)
	return state.convert_to_json()


@app.route('/getcurrent', methods = ['GET'])
def getcurrent():
	return state.convert_to_json()


@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json(force=True)
	print(data)
	result = ''

	for item in data:
		# loop over every row
		result += str(item['make']) + '\n'

	return result

if __name__ == '__main__':


	## Parse the command line options
	parser = ArgumentParser()

	parser.add_argument("-i", "--interactive",
						dest="interactive",
						help="Which phase the game should start at.",
						action="store_true")

	# player 1 & 2
	parser.add_argument("-1", "--player1",
						dest="player1",
						help="the program to run for player 1 (default: rand). Note: only set player 1 if you are not playing interactively",
						default="rand")

	parser.add_argument("-2", "--player2",
						dest="player2",
						help="the program to run for player 2 (default: rand)",
						default="rand")



	options = parser.parse_args()

	state = None
	player1 = util.load_player(options.player1)
	player2 = util.load_player(options.player2)


	app.run(debug=True)
