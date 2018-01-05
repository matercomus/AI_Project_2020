"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State
from api import Deck
import random


class Bot:

	def __init__(self):
		pass

	def get_move(self, state):
		# type: (State) -> tuple[int, int]
		"""
		Function that gets called every turn. This is where to implement the strategies.
		Be sure to make a legal move. Illegal moves, like giving an index of a card you
		don't own or proposing an illegal mariage, will lose you the game.
		TODO: add some more explanation
		:param State state: An object representing the gamestate. This includes a link to
			the states of all the cards, the trick and the points.
		:return: A tuple of integers or a tuple of an integer and None,
			indicating a move; the first indicates the card played in the trick, the second a
			potential spouse.
		"""
		#TODO: not finished at all, will continue working on it (Geoffrey)
		# All legal moves
		moves = state.moves()
		chosen_move = None
		if state.get_opponents_card() is None:
			chosen_move = moves[0]

			moves_trump_suite = []
			for index, move in enumerate(moves):
				if move[0] is not None and Deck.get_suit(move[0]) == state.get_deck().get_trump_suit():
					moves_trump_suite.append(move)

			if len(moves_trump_suite) > 0:
				print "The trump suite cards are\n{}".format(moves_trump_suite)
				chosen_move = moves_trump_suite[0]
			else:
				chosen_move = moves[0]
				for index, move in enumerate(moves):
					if move[0] is not None and moves[0][0] % 5 > move[0] % 5:
						print "{} is bigger than {}".format(moves[0][0], move[0])
						chosen_move = move
				print "The moves that are available are \n{}.".format(moves)
				print "The chosen move was \n{}".format(chosen_move)
				# chosen_move = random.choice(moves)


			# for i in range(len(moves) - 1):
			# 	if moves[i][0] is not None and state.get_deck().get_rank(chosen_move[0]) < state.get_deck().get_rank(
			# 			moves[i][0]):
			# 		chosen_move = moves[i]
		else:
			chosen_move = random.choice(moves)

		# chosen_move = moves[0]

		# print chosen_move
		# print state.get_deck().get_card_states()
		# Return a random choice
		return chosen_move