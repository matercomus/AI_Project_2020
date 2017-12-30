from unittest import TestCase

from api import Deck, _state


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
		state = _state.State(deck,True)
		clone = state.clone()

		self.assertEqual(state.finished(), clone.finished())

		self.assertEqual(state.revoked(), clone.revoked())

		self.assertEqual(state.winner(), clone.winner())

		current_deck = state.get_deck()
		clone_deck = clone.get_deck()
		self.assertEqual(current_deck.getCardState(), clone_deck.getCardState())


		pass
