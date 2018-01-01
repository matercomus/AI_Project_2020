from . import State, Deck, util
from numpy import random

state = State.generate()

for i in range(5):
	moves = state.moves()
	print state
	print state.get_deck().get_card_states()
	state = state.next(random.choice(moves))