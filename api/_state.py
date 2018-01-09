from api import util, Deck
import random


class State:
	__deck = None  # type: Deck

	__phase = None # type: int

	__leads_turn = None  # type: bool

	__player1s_turn = None  # type: bool

	__p1_points = None  # type: int
	__p2_points = None  # type: int

	__p1_pending_points = None #type: int
	__p2_pending_points = None #type: int

	__p1_perspective = None #type: list[str]
	__p2_perspective = None #type: list[str]

	__revoked = None  # type: int, None

	def __init__(self,
				 deck,
				 player1s_turn,
				 p1_points=0,
				 p2_points=0,
				 p1_pending_points=0,
				 p2_pending_points=0,
				 p1_perspective=None,
				 p2_perspective=None
				 ):
		"""
		:param deck:			The Deck object which holds the full deck state.
		:param player1s_turn:	A boolean indicating whether it is player 1's turn or not
		:param p1/2_points:		Integer variables that hold each player's current points
		:param p1/2_pending_points:	   Integer variables that hold each player's pending points
		:param p1/2_perspective:A list of strings which represents each player's perspective of the deck
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

		"""
		Computes the next state based on the given move

		:param move: Tuple of length 2 of which each element can either be an int or None
		:return: Newly computed state based on current state and given move
		"""

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

			# Store the indices we need in variables
			trump_jack_index = move[1]
			trump_card_index = state.__get_deck().get_trump_card_index()

			# Perform trump jack exchange
			state.__exchange_trump(trump_jack_index)


			# Update perspectives with information gained in trump jack exchange
			state.__add_to_perspective(1, trump_card_index, state.__get_deck().get_card_state(trump_card_index))
			state.__add_to_perspective(2, trump_card_index, state.__get_deck().get_card_state(trump_card_index))

			state.__add_to_perspective(1, trump_jack_index, state.__get_deck().get_card_state(trump_jack_index))
			state.__add_to_perspective(2, trump_jack_index, state.__get_deck().get_card_state(trump_jack_index))

			# Do not change turns before returning state, since trump jack exchange does not use a turn.
			return state

		# Change turns
		state.__leads_turn = not state.__leads_turn

		#Add the given move to the trick, store the whole trick in a variable
		trick = state.__get_deck().set_trick(state.whose_turn(), move[0])

		# At this point, we know that the move is not a trump jack exchange.
		# Check if this move is a marriage
		if move[1] is not None:

			# A marriage cannot be melded by the non-leading player
			if state.__leads_turn:
				raise RuntimeError("Marriage was attempted to be melded by non-leading player")

			# Update perspective since an additional card is revealed by the player who performs a marriage.
			state.__add_to_perspective(util.other(state.whose_turn()), move[1], "P" + str(state.whose_turn()) + "H")

			# Trump suit marriage yields 40 points, regular yields 20, to be awarded at next trick win.
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

		#Draw cards from stock
		if state.__phase == 1:
			state.__get_deck().draw_card(leader)
			state.__get_deck().draw_card(util.other(leader))
			if state.__get_deck().get_stock_size() == 0:
				state.__phase = 2


		# Set player1s_turn according to the leader variable
		state.__player1s_turn = True if leader == 1 else False

		# Returns state
		return state

	def finished(self):
		"""
		:return: Boolean indicating whether current state is finished or not
		"""
		if self.__revoked is not None:
			return True

		if self.__p1_points >= 66 or self.__p2_points >= 66:
			return True

		return False

	def revoked(self):
		"""
		:return: Integer indicating player id of player who made an illegal move, or None if not revoked
		"""
		return self.__revoked

	def winner(self):
		"""
		Who won the game (if it's finished).

		:return: The (integer) id of the player who won if the game is finished (1 or 2). (None, None)
			if the game is not finished.
		"""

		winner = None
		points = None

		if self.__revoked is not None:
			return self.whose_turn(), 3

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
			A move is a tuple of length 2. There are 3 distinct cases:
				- (int, None): first element indicates the index of the card that is placed down.
				- (int, int) : first element as above, second element completes a marriage
				- (None, int): First element being None indicates a trump jack exchange,
					second element is the index of that trump jack
		"""

		hand = self.__get_deck().get_player_hand(self.whose_turn())
		possible_moves = []

		# In this case, no constraints are put on the move
		if self.__phase == 1 or self.whose_turn() == self.leader():

			for card in hand:
				possible_moves.append((card, None))

			#If the player is able to exchange their trump Jack, then this option will be added to the possible moves.
			if self.__deck.can_exchange(self.whose_turn()):
				possible_moves.append((None, self.__deck.get_trump_jack_index()))

		# If the game is in phase 2 and it's not the leader's turn, then some constraints apply
		else:
			opponent_card = self.get_opponents_played_card()
			same_suit_hand = [card for card in hand if Deck.get_suit(card) == Deck.get_suit(opponent_card)]
			playable_cards = None

			if len(same_suit_hand) > 0:
				same_suit_hand_higher = [card for card in same_suit_hand if card < opponent_card]

				if len(same_suit_hand_higher) > 0:
					playable_cards = same_suit_hand_higher
				else:
					playable_cards = same_suit_hand


			elif Deck.get_suit(opponent_card) != self.__get_deck().get_trump_suit():
				trump_hand = [card for card in hand if Deck.get_suit(card) == self.__get_deck().get_trump_suit()]
				if len(trump_hand) > 0:
					playable_cards = trump_hand
				else:
					playable_cards = hand
			else:
				playable_cards = hand

			possible_moves = [(card, None) for card in playable_cards]

		#Add possible mariages to moves
		#Marriages can only be melded by leader
		if self.whose_turn() == self.leader():
			possible_mariages = self.__get_deck().get_possible_mariages(self.whose_turn())
			possible_moves += possible_mariages

		return possible_moves

	# Implementation will be changed in W2
	def hand(self):
		"""
		:return: An array of indices representing the cards in the current player's hand
		"""
		return self.__deck.get_player_hand(self.whose_turn())


	def clone(self):
		"""
		:return: Returns a deep copy of the current state
		"""
		state = State(self.__get_deck().clone(), self.__player1s_turn, self.__p1_points, self.__p2_points, self.__p1_pending_points, self.__p2_pending_points, list(self.__p1_perspective), list(self.__p2_perspective))
		state.__phase = self.__phase
		state.__leads_turn = self.__leads_turn
		state.__revoked = self.__revoked

		return state

	@staticmethod
	def generate(id=None, phase=1):
		"""
		:param id: The seed used for random generation. Defaults at random, but can be set for deterministic state generation
		:param phase: The phase at which your generated state starts at
		:return: A starting state generated using the parameters given
		"""

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
		rep += "Player 1's hand:"

		for card in self.__deck.get_player_hand(1):
			rank, suit = util.get_card_name(card)
			rep += " {}{}".format(rank, suit)

		rep += "\n"
		rep += "Player 2's hand:"

		for card in self.__deck.get_player_hand(2):
			rank, suit = util.get_card_name(card)
			rep += " {}{}".format(rank, suit)

		rep += "\n"
		rep += "There are {} cards in the stock\n".format(self.__get_deck().get_stock_size())
		
		trick = self.__get_deck().get_trick()
		if trick[0] is not None:
			rep += "Player 1 has played card: {} of {}\n".format(util.get_rank(trick[0]), util.get_suit(trick[0]))
		if trick[1] is not None:
			rep += "Player 2 has played card: {} of {}\n".format(util.get_rank(trick[1]), util.get_suit(trick[1]))

		return rep

	def is_valid(self, move):
		"""
		:param move: tuple representing move
		:return: A boolean indicating whether the given move is valid considering the current state
		"""
		if (self.__phase == 1 or self.__leads_turn) and move[0] is not None and move[1] is None:
			return (self.__get_deck().get_card_state(move[0]) == ("P" + str(self.whose_turn()) + "H"))
		return move in self.moves()

	def get_opponents_played_card(self):
		"""
		:return: An integer representing the index of the card the opponent has played, None if no card played
		"""
		return self.__get_deck().get_trick()[util.other(self.whose_turn()) - 1]

	def whose_turn(self):
		"""
		:return: The player id whose turn it is currently
		"""
		return 1 if self.__player1s_turn else 2

	# TODO: Restrict to only current player's perspective
	def get_perspective(self, player):
		"""
		:param player: The player id of the player whose perspective we want
		:return: The perspective list of the indicated player
		"""
		return self.__p1_perspective if player == 1 else self.__p2_perspective

	def leader(self):
		"""
		:return: An integer representing the player id of the current leader
		"""
		return 1 if self.__leads_turn == self.__player1s_turn else 2

	def get_points(self, player):
		"""
		:param player: The player id of the player whose points we want
		:return: The points of the requested player
		"""
		return self.__p1_points if player == 1 else self.__p2_points

	def get_pending_points(self, player):
		"""
		:param player: The player id of the player whose pending points we want
		:return: The pending points of the requested player
		"""
		return self.__p1_pending_points if player == 1 else self.__p2_pending_points

	def get_trump_suit(self):
		"""
		:param player: The player id of the player whose points we want
		:return: The points of the requested player
		"""
		return self.__deck.get_trump_suit()

	def get_stock_size(self):
		"""
		:return: The size of the stock
		"""
		return self.__deck.get_stock_size()

	def __exchange_trump(self, trump_jack_index):
		"""
		Exchanges the trump card with the trump Jack.

		:param trump_jack_index: An integer signifying the index of the trump Jack
		"""
		self.__deck.exchange_trump(trump_jack_index)

	def __get_deck(self):
		"""
		:return: The deck in the state
		"""
		return self.__deck

	def __set_points(self, player, points):
		"""
		Sets the point count of the specified player to the specified points

		:param player: An integer signifying the player id
		:param player: An integer signifying the point count to player's points are set to
		"""

		if player == 1:
			self.__p1_points = points
		else:
			self.__p2_points = points

	def __add_points(self, player, points):
		"""
		Adds the specified points to the point count of the specified player

		:param player: An integer signifying the player id
		:param player: An integer signifying the points to be added to the point count of the player
		"""

		if player == 1:
			self.__p1_points += points
		else:
			self.__p2_points += points

	def __reserve_pending_points(self, player, points):
		"""
		Adds the specified pending points to the pending point count of the specified player

		:param player: An integer signifying the player id
		:param player: An integer signifying the pending points to be added to the pending point count of the player
		"""
		if player == 1:
			self.__p1_pending_points += points
		else:
			self.__p2_pending_points += points

	def __add_pending_points(self, player):
		"""
		Adds the pending points of the specified player to that player's points
		:param player: An integer signifying the player id
		"""

		if player == 1:
			self.__p1_points += self.__p1_pending_points
			self.__p1_pending_points = 0
		else:
			self.__p2_points += self.__p2_pending_points
			self.__p2_pending_points = 0

	def __allocate_trick_points(self, winner, trick):
		"""
		:param winner: The player id of the player who won the trick
		:param trick: A tuple signifying the trick which is used to determine how many points the winner is allocated
		"""

		# A list containing points of the cards of by rank
		score = [11, 10, 4, 3, 2]

		rank_first_card_trick = trick[0] % 5
		rank_second_card_trick = trick[1] % 5

		total_score = score[rank_first_card_trick]
		total_score += score[rank_second_card_trick]

		self.__add_points(winner, total_score)
		self.__add_pending_points(winner)

	def __add_to_perspective(self, player, index, card_state):
		"""
		Changes the specified player's perspective of the card at the given index to the given card state

		:param player: An integer signifying the player id
		:param index: An integer signifying the index of a card
		:param card_state: A string signifying the state of the card
		"""

		if player == 1:
			self.__p1_perspective[index] = card_state
		else:
			self.__p2_perspective[index] = card_state

	def __add_partial_trick_to_perspective(self, trick, player):
		"""
		Adds the card in the trick to the specified player's perspective

		:param trick: A tuple signifying the trick which cards are revealed to the player
		:param player: An integer signifying the player id
		"""

		if player == 1:
			self.__p1_perspective[trick[util.other(player) - 1]] = "P2H"
		else:
			self.__p2_perspective[trick[util.other(player) - 1]] = "P1H"

	def __alter_perspective(self, trick, winner):
		"""
		Adds the cards in the trick to both players' perspective as in the won cards pile of the specified winner

		:param trick: A tuple signifying the trick which cards are revealed to both players
		:param winner: An integer signifying the winner's id
		"""

		if winner == 1:
			self.__p1_perspective[trick[0]] = self.__p1_perspective[trick[1]] = "P1W"
			self.__p2_perspective[trick[0]] = self.__p2_perspective[trick[1]] = "P1W"

		else:
			self.__p1_perspective[trick[0]] = self.__p1_perspective[trick[1]] = "P2W"
			self.__p2_perspective[trick[0]] = self.__p2_perspective[trick[1]] = "P2W"

	def __evaluate_trick(self, trick):
		"""
		Evaluates who the winner of the specified trick is and returns it

		:param trick: A tuple signifying the trick which is evaluated
		:return: The winner's id as an integer
		"""

		if len(trick) != 2:
			raise RuntimeError("Incorrect trick format. List of length 2 needed.")
		if trick[0] is None or trick[1] is None:
			raise RuntimeError("An incomplete trick was attempted to be evaluated.")
		
		# If the two cards of the trick have the same suit
		if Deck.get_suit(trick[0]) == Deck.get_suit(trick[1]):

			# We only compare indices since the convention we defined in Deck 
			# puts higher rank cards at lower indices, when considering the same color.
			return 1 if trick[0] < trick[1] else 2

		if Deck.get_suit(trick[0]) ==  self.__get_deck().get_trump_suit():
			return 1

		if Deck.get_suit(trick[1]) ==  self.__get_deck().get_trump_suit():
			return 2

		# If the control flow has reached this point, the trick consists of two
		# different non-trump cards. Since the new leader is determined by the
		# output of this function, at this point the state object still considers
		# it to be the non-leading player's turn. Thus, we determine that the winner
		# is the other player, i.e. the leading player. Thanks: Daan Raven
		return util.other(self.whose_turn())
