from api import util

class State:

	__deck = None # type: Deck

	__leadsTurn = None # type: bool

	__player1sTurn = None # type: bool

	__p1Points = None # type: int
	__p2Points = None # type: int

	__revoked = None #type: int, None

	def __init__(self,
				 deck,		 # type: Deck
				 player1sTurn,		 # type: bool
				 p1Points=0, # type: int
				 p2Points=0	 # type: int
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
		self.__player1sTurn = player1sTurn
		self.__leadsTurn = True

		self.__p1Points = p1Points
		self.__p2Points = p2Points

	def next(self,
	 move   # type: tuple(int, int)
	):
	# type: () -> State
	"""
	Compute the next state from this one, assuming that the player whose turn it is makes the given move.

	:return: The state that would result from the given move.
	:raises: RuntimeError if state is finished. Be sure to check state.finished() before calling this
	method.
	"""

        if self.finished():
            raise RuntimeError('Gamestate is finished. No next states exist.')

        # Start with a copy of the current state
        state = self.clone() # type: State

        state.__leadsTurn = not state.__leadsTurn

        if state.__leadsTurn:
        	#Figure out who new lead is by checking who won last trick

        if not is_valid(move):
        	state.__revoked





	def finished(self):

		if self.__revoked is not None:
			return True

		if self.__p1Points >= 66 || self.__p2Points >= 66:
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

        if self.__p1Points >= 66:

        	winner = 1
        	if self.__p2Points == 0:
        		points = 3

        	elif self.__p2Points < 33:
        		points = 2

        	else:
        		points = 1

        elif self.__p2Points >= 66:

        	winner = 2
        	if self.__p1Points == 0:
        		points = 3

        	elif self.__p1Points < 33:
        		points = 2

        	else:
        		points = 1

        return winner, points

    def clone(self):
    	state = State(self.__deck.clone(), self.__player1sTurn, self.__p1Points, self.__p2Points)
    	state.__leadsTurn = self.__leadsTurn
    	state.__revoked = self.__revoked

    	return state

    def is_valid(self):
    	pass












