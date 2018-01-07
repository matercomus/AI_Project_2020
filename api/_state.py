from api import util, Deck
import random

# TODO:
# IMPORTANT: MAKE PRIVATE METHODS


# Low priority/style:
# Change all method calls of class variables from within the class to the variables themselves
# Add constants for player 1 and player 2 so that we don't have to use 1 and 2

# Following the previous idea, could alter the card states to hold state codes that would be kept
# in static class variables. Actually I think this is something we need to do before we go to production

# Maybe turn __phase into a boolean, since it can only take two values. Would be cleaner


class State:
	__deck = None  # type: Deck

	__phase = None

	__leads_turn = None  # type: bool

	__player1s_turn = None  # type: bool

	__p1_points = None  # type: int
	__p2_points = None  # type: int

	__p1_pending_points = None
	__p2_pending_points = None


	# Decided to put the perspectives in State because they are more of a
	# construct over the real deck state, and because they relate to the players
	# of the game, which we've kept out of the deck so far.

	__p1_perspective = None
	__p2_perspective = None

	__revoked = None  # type: int, None

	def __init__(self,
				 deck,  # type: Deck
				 player1s_turn,  # type: bool
				 p1_points=0,  # type: int
				 p2_points=0,  # type: int
				 p1_pending_points=0,
				 p2_pending_points=0,
				 p1_perspective=None,
				 p2_perspective=None
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

		self.__p1_pending_points = p1_pending_points
		self.__p2_pending_points = p2_pending_points

		# If perspectives are not given in the constructor, they are computed:
		# If phase 1, all cards that are not either in the player's hand or won already,
		# or the revealed trump card on the bottom of the stock, are unknown.
		# If phase 2, everything is known, so deck.__card_state is simply copied over.
		# This is all that can be deduced from a card state array, but further knowledge
		# can be gathered through trump jack exchanges or marriages, which is implemented
		# in the player's perspective in state transitions.

		if p1_perspective is None:
			if self.__phase == 1:
				p1_perspective = [card if ((card != "S" or index == deck.get_stock()[0]) and card != "P2H") else "U" for index, card in enumerate(deck.get_card_states())]
			else:
				p1_perspective = deck.get_card_states()

		if p2_perspective is None:
			if self.__phase == 1:
				p2_perspective = [card if ((card != "S" or index == deck.get_stock()[0]) and card != "P1H") else "U" for index, card in enumerate(deck.get_card_states())]
			else:
				p2_perspective = deck.get_card_states()

		self.__p1_perspective = p1_perspective
		self.__p2_perspective = p2_perspective

	def next(self,
			 move  # type: tuple(int, int)
			 ):

		if self.finished():
			raise RuntimeError('Gamestate is finished. No next states exist.')

		# Start with a copy of the current state
		state = self.clone()  # type: State

		# If we find an invalid move, we set the __revoked class variable
		# To the pid of the player who made the incorrect move, and return the state as is.
		if not state.is_valid(move):
			state.__revoked = state.whose_turn()
			return state

		# If move is a trump exchange
		if move[0] is None:
			# TODO: ADD TO PERSPECTIVE

			# state.__add_to_perspective()

			trump_jack_index = move[1]
			trump_card_index = state.__get_deck().get_trump_card_index()

			state.__exchange_trump(trump_jack_index)

			state.__add_to_perspective(1, trump_card_index, state.__get_deck().get_card_state(trump_card_index))
			state.__add_to_perspective(2, trump_card_index, state.__get_deck().get_card_state(trump_card_index))

			state.__add_to_perspective(1, trump_jack_index, state.__get_deck().get_card_state(trump_jack_index))
			state.__add_to_perspective(2, trump_jack_index, state.__get_deck().get_card_state(trump_jack_index))

			return state

		# Change turns
		state.__leads_turn = not state.__leads_turn

		#Add the given move to the trick, store the whole trick in a variable
		trick = state.__get_deck().set_trick(state.whose_turn(), move[0])

		if move[1] is not None:

			if state.__leads_turn:
				raise RuntimeError("Marriage was attempted to be melded by non-leading player")

			state.__add_to_perspective(util.other(state.whose_turn()), move[1], "P" + str(state.whose_turn()) + "H")

			if Deck.get_suit(move[1]) == state.__get_deck().get_trump_suit():
				state.__reserve_pending_points(state.whose_turn(), 40)
			else:
				state.__reserve_pending_points(state.whose_turn(), 20)

		#If it is not the lead's turn, i.e. currently the trick is incomplete
		if not state.__leads_turn:
			state.__player1s_turn = not state.__player1s_turn
			state.__add_partial_trick_to_perspective(trick, state.whose_turn())
			return state

		# At this point we know that it is the lead's turn and that a complete
		# trick from the previous hand can be evaluated.

		# Evaluate the trick and store the winner in the leader variable
		leader = state.__evaluate_trick(trick)

		state.__allocate_trick_points(leader, trick)

		state.__get_deck().put_trick_away(leader)

		state.__alter_perspective(trick, leader)

		if len(state.__get_deck().get_player_hand(1)) == 0 and not state.finished():
			# If all cards are exhausted, the winner of the last trick wins the game
			state.__set_points(leader, 66)

		#Draw cards
		#TODO: Clean up
		if state.__phase == 1:
			state.__get_deck().draw_card(leader)
			state.__get_deck().draw_card(util.other(leader))
			if state.__get_deck().get_stock_size() == 0:
				state.__phase = 2


		# Set player1s_turn according to the leader variable
		state.__player1s_turn = True if leader == 1 else False


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


	def moves(self):
		"""
		:return: A list of all the legal moves that can be made by the player whose turn it is.
		"""

		hand = self.__get_deck().get_player_hand(self.whose_turn())
		possible_moves = []

		if self.__phase == 1 or self.whose_turn() == self.leader():
			

			for card in hand:
				possible_moves.append((card, None))

			#If the player is able to exchange their trump Jack, then this option will be added to the possible moves.
			if self.__deck.can_exchange(self.whose_turn()):
				possible_moves.append((None, self.__deck.get_trump_jack_index()))
			# return possible_moves

		else:
			opponent_card = self.get_opponents_played_card()
			same_suit_hand = [card for card in hand if Deck.get_suit(card) == Deck.get_suit(opponent_card)]

			if len(same_suit_hand) > 0:
				same_suit_hand_higher = [card for card in same_suit_hand if card < opponent_card]

				if len(same_suit_hand_higher) > 0:
					possible_moves = [(x, None) for x in same_suit_hand_higher]
				else:
					possible_moves = [(x, None) for x in same_suit_hand]


			elif Deck.get_suit(opponent_card) != self.__get_deck().get_trump_suit():
				trump_hand = [card for card in hand if Deck.get_suit(card) == self.__get_deck().get_trump_suit()]
				if len(trump_hand) > 0:
					possible_moves = [(x, None) for x in trump_hand]
				else:
					possible_moves = [(x, None) for x in hand]
			else:
				possible_moves = [(x, None) for x in hand]


		#Add possible mariages to moves
		#Marriages can only be melded by leader
		if self.whose_turn() == self.leader():
			possible_mariages = self.__get_deck().get_possible_mariages(self.whose_turn())
			possible_moves += possible_mariages

		return possible_moves


	def clone(self):
		state = State(self.__get_deck().clone(), self.__player1s_turn, self.__p1_points, self.__p2_points, self.__p1_pending_points, self.__p2_pending_points, list(self.__p1_perspective), list(self.__p2_perspective))
		state.__phase = self.__phase
		state.__leads_turn = self.__leads_turn
		state.__revoked = self.__revoked

		return state


	@staticmethod
	def generate(id=None, phase=1):

		if id is None:
			id = random.randint(0, 100000)
		rng = random.Random(id)
		deck = Deck.generate(id)
		player1s_turn = rng.choice([True, False])

		state = State(deck, player1s_turn)

		if phase == 2:
			while state.__phase == 1:
				if state.finished():
					return State.generate(id+1, phase) # Father forgive me

				state = state.next(rng.choice(state.moves()))

		return state

	def __repr__(self):
		# type: () -> str
		"""
		:return: A concise string representation of the state in one line
		"""

		rep = "The game is in phase: {}\n".format(self.__phase)
		rep += "Player 1's points: {}, pending: {}\n".format(self.__p1_points, self.__p1_pending_points)
		rep += "Player 2's points: {}, pending: {}\n".format(self.__p2_points, self.__p2_pending_points)
		rep += "There are {} cards in the stock".format(self.__get_deck().get_stock_size())

		return rep


	#TODO Maybe change card_state array to something less terrible to compare to
	#Maybe move to deck
	def is_valid(self, move):
		if (self.__phase == 1 or self.__leads_turn) and move[0] is not None and move[1] is None:
			return (self.__get_deck().get_card_state(move[0]) == ("P" + str(self.whose_turn()) + "H"))
		return move in self.moves()

	def get_opponents_played_card(self):
		return self.__get_deck().get_trick()[util.other(self.whose_turn()) - 1]

	def whose_turn(self):
		return 1 if self.__player1s_turn else 2

	def get_perspective(self, player):
		return self.__p1_perspective if player == 1 else self.__p2_perspective

	def leader(self):
		return 1 if self.__leads_turn == self.__player1s_turn else 2

	def get_points(self, player):
		return self.__p1_points if player == 1 else self.__p2_points

	def get_pending_points(self, player):
		return self.__p1_pending_points if player == 1 else self.__p2_pending_points

	def __exchange_trump(self, trump_jack_index):
		self.__deck.exchange_trump(trump_jack_index)

	def __get_deck(self):
		return self.__deck

	def __set_points(self, player, points):
		if player == 1:
			self.__p1_points = points
		else:
			self.__p2_points = points

	def __add_points(self, player, points):
		if player == 1:
			self.__p1_points += points
		else:
			self.__p2_points += points

	def __reserve_pending_points(self, player, points):
		if player == 1:
			self.__p1_pending_points += points
		else:
			self.__p2_pending_points += points


	def __add_pending_points(self, player):
		if player == 1:
			self.__p1_points += self.__p1_pending_points
			self.__p1_pending_points = 0
		else:
			self.__p2_points += self.__p2_pending_points
			self.__p2_pending_points = 0

	# Maybe good to merge this with __add_pending_points
	def __allocate_trick_points(self, winner, trick):
		score = [11, 10, 4, 3, 2]

		# TODO: CLEAN UP, ADD EXPLANATION
		total_score = score[trick[0] % 5]
		total_score += score[trick[1] % 5]

		self.__add_points(winner, total_score)
		self.__add_pending_points(winner)

	def __add_to_perspective(self, player, index, state):
		if player == 1:
			self.__p1_perspective[index] = state
		else:
			self.__p2_perspective[index] = state

	#Alters perspective with only a partial trick
	def __add_partial_trick_to_perspective(self, trick, player):
		if player == 1:
			self.__p1_perspective[trick[util.other(player) - 1]] = "P2H"
		else:
			self.__p2_perspective[trick[util.other(player) - 1]] = "P1H"


	#Alters perpsective with a complete trick
	def __alter_perspective(self, trick, winner):

		if winner == 1:
			self.__p1_perspective[trick[0]] = self.__p1_perspective[trick[1]] = "P1W"
			self.__p2_perspective[trick[0]] = self.__p2_perspective[trick[1]] = "P1W"

		else:
			self.__p1_perspective[trick[0]] = self.__p1_perspective[trick[1]] = "P2W"
			self.__p2_perspective[trick[0]] = self.__p2_perspective[trick[1]] = "P2W"



	#Evaluate a complete trick, assign points and return the pid of the winner
	def __evaluate_trick(self, trick):
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

		if Deck.get_suit(trick[0]) ==  self.__get_deck().get_trump_suit():
			return 1

		if Deck.get_suit(trick[1]) ==  self.__get_deck().get_trump_suit():
			return 2

		return self.whose_turn()