from api import State, Deck, util
from numpy import random

state = State.generate()

print "Trump suit: " + state.get_deck().get_trump_suit()


for i in range(5):
	moves = state.moves()
	print state
	print state.get_deck().get_card_states()
	print state.get_deck().get_trick()
	print str(state.leader()) + " " + str(state.whose_turn())
	state = state.next(moves[0])