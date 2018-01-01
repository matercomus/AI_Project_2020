from unittest import TestCase

from api import Deck, State


class TestState(TestCase):
	def test_next(self):
		# TODO: add sth?
		pass

	def test_finished(self):
		# TODO: add sth?
		pass

	def test_possible_move(self):
		#TODO implement after possible_move
		pass

	def test_next(self):
		# TODO implement after next
		pass

	def test_clone(self):
		deck = Deck.generate()
		state = State(deck,True)
		clone = state.clone()

		self.assertEqual(state.finished(), clone.finished())

		self.assertEqual(state.revoked(), clone.revoked())

		self.assertEqual(state.winner(), clone.winner())

		current_deck = state.get_deck()
		clone_deck = clone.get_deck()
		self.assertEqual(current_deck.get_card_states(), clone_deck.get_card_states())


		pass

	def test_game10(self):
		state = State.generate()

		for i in range(10):
			moves = state.moves()
			state = state.next(moves[0])

	def test_game15(self):
		state = State.generate()

		for i in range(15):
			print state
			moves = state.moves()
			state = state.next(moves[0])

	def test_game_full(self):

		for i in range(1000):
			state = State.generate()
			while not state.finished():
				moves = state.moves()
				print state.get_deck().get_card_states()
				print "p1 score: {}".format(state.get_points(1))
				print "p2 score: {}".format(state.get_points(2))
				print moves
				state = state.next(moves[0])