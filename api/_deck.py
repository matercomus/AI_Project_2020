from numpy import random

class Deck:
	"""
	Represents the deck at any given turn.
	"""

	__RANKS = ["A", "10", "K", "Q", "J"]
	__SUITS = ["C", "D", "H", "S"]

	# A list of length 20 representing all cards and their states
	__cardState = None # type: list[str]

	#We use the following index representations for cards:

	# Suit order: CLUBS, DIAMONDS, HEARTS, SPADES

	# 0, 5, 10, 15 - Aces
	# 1, 6, 11, 16 - 10s
	# 2, 7, 12, 17 - Kings
	# 3, 8, 13, 18 - Queens
	# 4, 9, 14, 19 - Jacks

	# A variable length list of card indexes representing the
	# cards currently in stock, and more importantly, their order.
	# First index in this list is always the trump card, last index
	# is where the cards are taken from the stock.
	__stock = None # type: list[int]

	# The suit of the trump card for this given deck instance.
	__trump = None # type: String

	def __init__(self,
				cardState,	# type: list[str]
				stock,		# type: list[int]
				trump 		# type: str
				):
		"""
		:param cardState: list of current card states
		:param stock: list of indexes of cards in stock
		:param trump: {C,D,H,S}
		"""

		self.__cardState = cardState
		self.__stock 	 = stock
		self.__trump 	 = trump


	# Computes the rank of a given card index, following the ordering given above.
	@staticmethod
	def getRank(index):
		return Deck.__RANKS[index % 5]
		

	# Computes the suit of a given card index, following the ordering given above.
	@staticmethod
	def getSuit(index):
		return Deck.__SUITS[int(index/5)]

	def getCardState(self):
		return self.__cardState

	def setCard(self, index, state):
		self.__cardState[index] = state


	@staticmethod
	def generate():

		shuffledCards = random.permutation(range(20))

		cardState = [0]*20
		stock = [] # Can be thought of as a stack data structure.

		# Three separate for loops assign a state to the cards in the
		# shuffled deck depending on their position. The indices of the
		# stock cards are pushed onto the stock stack to save their order.
		for i in range(10):
			cardState[shuffledCards[i]] = "Stock"
			stock.append(shuffledCards[i])

		for i in range(10, 15):
			cardState[shuffledCards[i]] = "P1Hand"

		for i in range(15, 20):
			cardState[shuffledCards[i]] = "P2Hand"

		trump = Deck.getSuit(shuffledCards[0])

		return Deck(cardState, stock, trump)

	def clone(self):
		deck = Deck(list(self.__cardState), list(self.__stock), self.__trump)
		return deck

