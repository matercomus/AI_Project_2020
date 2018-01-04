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
		deck = Deck.generate(0)
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
		state = State.generate(0)

		for i in range(10):
			if not state.finished():
				moves = state.moves()
				state = state.next(moves[0])

	def test_game15(self):
		state = State.generate(0)

		for i in range(15):
			if not state.finished():
				# print state
				moves = state.moves()
				state = state.next(moves[0])

	def test_game_full(self):
		wins = 0
		for i in range(1000):
			state = State.generate(0)
			while not state.finished():
				moves = state.moves()
				# print state.get_deck().get_card_states()
				# print "p1 score: {}".format(state.get_points(1))
				# print "p2 score: {}".format(state.get_points(2))
				# print moves
				state = state.next(moves[0])

			winner, points = state.winner()
			if winner == 1:
				wins +=1
		print wins

	def test_seed_same(self):
		for i in range(1,1000):
			id = i
			s = State.generate(id)
			s1 = State.generate(id)
			if s.get_deck().get_card_states() != s1.get_deck().get_card_states() or s.whose_turn() != s.whose_turn():
				raise RuntimeError("The decks are not shuffled in the same way.")
				print s.get_deck().get_card_states()
				print s1.get_deck().get_card_states()

	def test_seed_different(self):
		s = State.generate(0)
		s1 = State.generate(0)
		if s.get_deck().get_card_states() == s1.get_deck().get_card_states():
			raise RuntimeError("The decks are shuffled in the same way.")
			print s.get_deck().get_card_states()
			print s1.get_deck().get_card_states()