from api import util


class State:
	__deck = None  # type: Deck

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
		self.__player1s_turn = player1s_turn
		self.__leads_turn = True

		self.__p1_points = p1_points
		self.__p2_points = p2_points

	def next(self,
			 move  # type: tuple(int, int)
			 ):

		if self.finished():
			raise RuntimeError('Gamestate is finished. No next states exist.')

		# Start with a copy of the current state
		state = self.clone()  # type: State

		# Change turns
		state.__leads_turn = not state.__leads_turn

		# If we find an invalid move, we set the __revoked class variable
		# To the pid of the player who made the incorrect move, and return the state as is.
		if not is_valid(move):
			state.__revoked = self.whose_turn()
			return state

		state.get_deck().set_trick(self.whose_turn(), move[0])

		#If it's now the lead's turn, i.e. a complete trick has been played
		if state.__leads_turn:

			# Evaluate the trick and store the winner in the leader variable
			leader = evaluate_trick(state.get_deck().get_trick())

			# Set player1s_turn according to the leader variable
			state.player1s_turn = True if leader == 1 else False

			#Clear the trick once evaluated to make room for the next one.
			state.get_deck().clear_trick()

		else:
			state.player1s_turn = not state.player1s_turn
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

	def clone(self):
		state = State(self.__deck.clone(), self.__player1s_turn, self.__p1_points, self.__p2_points)
		state.__leads_turn = self.__leads_turn
		state.__revoked = self.__revoked

		return state

	def is_valid(self, move):
		return True

	def get_deck(self):
		return self.__deck

	def whose_turn(self):
		return 1 if self.__player1s_turn else 2

	def get_points(self, player):
		return self.__p1_points if player == 1 else self.__p2_points

	#Evaluate a complete trick, assign points and return the pid of the winner
	def evaluate_trick(self, trick):
		if len(trick) != 2 or trick[0] is None or trick[1] is None
			raise RuntimeError("An incomplete trick was attempted to be evaluated")
		#TODO