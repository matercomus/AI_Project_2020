from api import util, Deck
from numpy import random

# TODO:
# Trump Jack exchange for trump card in the stock

class State:
	__deck = None  # type: Deck

	__phase = None

	__leads_turn = None  # type: bool

	__player1s_turn = None  # type: bool

	__p1_points = None  # type: int
	__p2_points = None  # type: int

	__revoked = None  # type: int, None

	def __init__(self,
				 deck,  # type: Deck
				 player1s_turn,  # type: bool
				 p1_points=0,  # type: int
				 p2_points=0  # type: int
				 ):
		"""
		:param map:		 The playing area
		:param garrisons:   A list of integers such that garrisons[i]
			contains the number of ships stationed at planet map.planets()[i]
		:param owner:	   A list of integers such that owners[i]
			contains the owner (0, 1 or 2) of planet  map.planets()[i]
		:param start:	   Which player is set to make the next turn in this state (1 or 2)
		:param fleets:	  A list of fleet objects representing the fleets in transit in this state
		"""
		self.__deck = deck

		self.__phase = 1 if len(deck.get_stock()) != 0 else 2

		self.__player1s_turn = player1s_turn
		self.__leads_turn = True

		self.__p1_points = p1_points
		self.__p2_points = p2_points

	#TODO: Implement marriages
	def next(self,
			 move  # type: tuple(int, int)
			 ):

		if self.finished():
			raise RuntimeError('Gamestate is finished. No next states exist.')

		# print "PLAYER 1 POINTS: " + str(self.__p1_points) + "; PLAYER 2 POINTS: " + str(self.__p2_points)

		# Start with a copy of the current state
		state = self.clone()  # type: State

		# Change turns
		state.__leads_turn = not state.__leads_turn

		# If we find an invalid move, we set the __revoked class variable
		# To the pid of the player who made the incorrect move, and return the state as is.
		if not self.is_valid(move):
			state.__revoked = self.whose_turn()
			return state

		print move
		state.get_deck().set_trick(self.whose_turn(), move[0])

		#If it's now the lead's turn, i.e. a complete trick has been played
		#Add evalMarriage() method
		if state.__leads_turn:


			# Evaluate the trick and store the winner in the leader variable
			trick = state.get_deck().get_trick()

			leader = state.evaluate_trick(trick)

			state.allocate_points(leader, trick)


			state.get_deck().put_trick_away(leader)

			#TODO: Clean up
			if state.__phase == 1:
				state.get_deck().draw_card(leader)
				state.get_deck().draw_card(util.other(leader))
				if state.get_deck().get_stock_size() == 0:
					state.__phase = 2



			# Set player1s_turn according to the leader variable
			state.__player1s_turn = True if leader == 1 else False

		else:
			state.__player1s_turn = not state.__player1s_turn
		# For Geoffrey: We need to think of a way to represent a trick that is
		# in the process of being played. We talked about adding 2 new possible states
		# to the cardStates array, but that might get messy. A simple way to do this would
		# be to have a list of length 2 called trick which would contain either [None, None] or
		# the indices of cards being played. This has the advantage that we don't have to
		# do list comprehension on a 20-element list potentially thousands of times, so this
		# is the way I will implement it, but feel free to change it if you think differently.

		return state

	def finished(self):

		if self.__revoked is not None:
			return True

		if self.__p1_points >= 66 or self.__p2_points >= 66:
			return True

		return False

	def revoked(self):
		return self.__revoked

	def winner(self):
		"""
		Who won the game (if it's finished).

		:return: The (integer) id of the player who won if the game is finished (1 or 2). None
			if the game is not finished.
		"""

		winner = None
		points = None

		if self.__p1_points >= 66:
			winner = 1
		elif self.__p2_points >= 66:
			winner = 2

		other_player_points = self.get_points(util.other(winner))

		if other_player_points == 0:
			points = 3
		elif other_player_points < 33:
			points = 2
		else:
			points = 1

		return winner, points

	# Add marriages, constrainst for 2nd phase
	def moves(self):
		"""
		:return: A list of all the legal moves that can be made by the player whose turn it is.
		"""

		hand = self.__deck.get_player_hand(self.whose_turn())

		if self.__phase == 1 or self.whose_turn() == self.leader():
			
			possible_moves = []

			for card in hand:
				possible_moves.append((card, None))

			return possible_moves

		else:
			opponent_card = self.__deck.get_trick()[util.other(self.whose_turn())-1]
			same_suit_hand = [card for card in hand if Deck.get_suit(card) == Deck.get_suit(opponent_card)]

			if len(same_suit_hand) > 0:
				same_suit_hand_higher = [card for card in same_suit_hand if card < opponent_card]

				if len(same_suit_hand_higher) > 0:
					return [(x, None) for x in same_suit_hand_higher]
					# return same_suit_hand_higher
				return [(x, None) for x in same_suit_hand]
				# return same_suit_hand

			elif Deck.get_suit(opponent_card) != self.__deck.get_trump_suit():
				trump_hand = [card for card in hand if Deck.get_suit(card) == self.__deck.get_trump_suit]
				if len(trump_hand) > 0:
					return [(x, None) for x in trump_hand]
					# return trump_hand
			return [(x, None) for x in hand]
			# return hand





	def clone(self):
		state = State(self.__deck.clone(), self.__player1s_turn, self.__p1_points, self.__p2_points)
		state.__phase = self.__phase
		state.__leads_turn = self.__leads_turn
		state.__revoked = self.__revoked

		return state

	@staticmethod
	def generate():
		deck = Deck.generate()
		player1s_turn = True if random.choice([1,2]) == 1 else False
		return State(deck, player1s_turn)


	def __repr__(self):
		# type: () -> str
		"""
		:return: A concise string representation of the state in one line
		"""

		rep = "The game is in phase: {}\n".format(self.__phase)
		rep += "Player 1's points: {}\n".format(self.__p1_points)
		rep += "Player 2's points: {}\n".format(self.__p2_points)
		rep += "There are {} cards in the stock".format(self.__deck.get_stock_size())

		return rep


	#TODO Actual move validation in the context of the rules of the game
	def is_valid(self, move):
		return True

	def get_deck(self):
		return self.__deck

	def whose_turn(self):
		return 1 if self.__player1s_turn else 2

	def leader(self):
		return 1 if self.__leads_turn == self.__player1s_turn else 2

	def get_points(self, player):
		return self.__p1_points if player == 1 else self.__p2_points

	def add_points(self, player, points):
		if player == 1:
			self.__p1_points += points
		else:
			self.__p2_points += points

	def allocate_points(self, winner, trick):
		score = [11, 10, 4, 3, 2]

		# TODO: CLEAN UP
		total_score = score[trick[0] % 5]
		total_score += score[trick[1] % 5]

		self.add_points(winner, total_score)


	#Evaluate a complete trick, assign points and return the pid of the winner
	#TODO: Make tests
	def evaluate_trick(self, trick):
		if len(trick) != 2:
			raise RuntimeError("Incorrect trick format. List of length 2 needed.")
		if trick[0] is None or trick[1] is None:
			raise RuntimeError("An incomplete trick was attempted to be evaluated.")
		
		# If the two cards of the trick have the same suit
		if Deck.get_suit(trick[0]) == Deck.get_suit(trick[1]):
			# If the two cards have the same suit, then we only consider rank,
			# since the convention we defined in Deck puts higher rank cards
			# at lower indices, when considering the same color.
			return 1 if trick[0] < trick[1] else 2

		if Deck.get_suit(trick[0]) ==  self.__deck.get_trump_suit():
			return 1

		if Deck.get_suit(trick[1]) ==  self.__deck.get_trump_suit():
			return 2

		return self.whose_turn()