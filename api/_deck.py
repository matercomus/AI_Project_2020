import random

class Deck:
	"""
	Represents the deck at any given turn.
	"""

	__RANKS = ["A", "10", "K", "Q", "J"]
	__SUITS = ["C", "D", "H", "S"]

	# A list of length 20 representing all cards and their states
	__card_state = None # type: list[str]

	#We use the following index representations for cards:

	# Suit order: CLUBS, DIAMONDS, HEARTS, SPADES

	# 0, 5, 10, 15 - Aces
	# 1, 6, 11, 16 - 10s
	# 2, 7, 12, 17 - Kings
	# 3, 8, 13, 18 - Queens
	# 4, 9, 14, 19 - Jacks

	# List that holds cards which are played at any one time.
	# Can contain two Nones, one None and an int, or two ints.
	# The ints represent the index of the played cards according to the scheme above.
	__trick = [None, None] # type: list[int], list[None]

	# A variable length list of card indexes representing the
	# cards currently in stock, and more importantly, their order.
	# First index in this list is always the trump_suit card, last index
	# is where the cards are taken from the stock.
	__stock = None # type: list[int]

	# The suit of the trump_suit card for this given deck instance.
	__trump_suit = None # type: String

	def __init__(self,
				card_state,	# type: list[str]
				stock,		# type: list[int]
				trump_suit 		# type: str
				):
		"""
		:param card_state: list of current card states
		:param stock: list of indexes of cards in stock
		:param trump_suit: {C,D,H,S}
		"""

		self.__card_state	= card_state
		self.__stock		= stock
		self.__trump_suit	= trump_suit


	# Computes the rank of a given card index, following the ordering given above.
	@staticmethod
	def get_rank(index):
		return Deck.__RANKS[index % 5]
		

	# Computes the suit of a given card index, following the ordering given above.
	@staticmethod
	def get_suit(index):
		return Deck.__SUITS[int(index/5)]

	def get_card_states(self):
		return list(self.__card_state)

	def get_card_state(self, index):
		return self.__card_state[index]

	def get_stock(self):
		return self.__stock

	def get_stock_size(self):
		return len(self.__stock)

	def set_card(self, index, state):
		self.__card_state[index] = state

	def get_trick(self):
		return list(self.__trick)

	def set_trick(self, player, card):
		self.__trick[player-1] = card
		return self.__trick

	def can_exchange(self, player):
		return self.__card_state[self.get_trump_jack_index()] == "P" + str(player) + "H"

	def get_player_hand(self, player_id):
		search_term = "P1H" if player_id == 1 else "P2H"
		return [i for i, x in enumerate(self.__card_state) if x == search_term]

	def get_trump_suit(self):
		return self.__trump_suit

	def exchange_trump(self, trump_jack_index):

		# trump_jack_index = self.get_trump_jack_index()

		self.__card_state[self.__stock[0]] = self.__card_state[trump_jack_index]

		self.__card_state[trump_jack_index] = "S"

		self.__stock[0] = trump_jack_index

	def get_trump_jack_index(self):

		#The Aces of different suits are always 5 apart from another Ace
		trump_ace_index = self.__SUITS.index(self.__trump_suit) * 5

		#The Jack of a suit is always 4 cards removed from the Ace of the same suit
		trump_jack_index = trump_ace_index + 4

		return trump_jack_index

	def get_possible_mariages(self, player):
		possible_mariages = []
		player_hand = self.get_player_hand(player)
		#TODO: quite bulky, maybe change into a more elegant solution or at the very least comment
		if 2 in player_hand and 3 in player_hand:
			possible_mariages.append((2, 3))
			possible_mariages.append((3, 2))
		if 7 in player_hand and 8 in player_hand:
			possible_mariages.append((7, 8))
			possible_mariages.append((8, 7))
		if 12 in player_hand and 13 in player_hand:
			possible_mariages.append((12, 13))
			possible_mariages.append((13, 12))
		if 17 in player_hand and 18 in player_hand:
			possible_mariages.append((17, 18))
			possible_mariages.append((18, 17))

		return possible_mariages

	def draw_card(self, player):
		if self.get_stock_size() == 0:
			raise RuntimeError('Stack is empty.')
		if player == 1:
			self.__card_state[self.__stock.pop()] = "P1H"
		else:
			self.__card_state[self.__stock.pop()] = "P2H"

	def put_trick_away(self, winner):
		if winner == 1:
			self.__card_state[self.__trick[0]] = self.__card_state[self.__trick[1]] = "P1W"
		else:
			self.__card_state[self.__trick[0]] = self.__card_state[self.__trick[1]] = "P2W"

		self.__trick = [None, None]





	# @staticmethod
	# def generate():
	#
	# 	shuffled_cards = random.permutation(range(20))
	#
	# 	card_state = [0]*20
	# 	stock = [] # Can be thought of as a stack data structure.
	#
	# 	# Three separate for loops assign a state to the cards in the
	# 	# shuffled deck depending on their position. The indices of the
	# 	# stock cards are pushed onto the stock stack to save their order.
	# 	for i in range(10):
	# 		card_state[shuffled_cards[i]] = "S"
	# 		stock.append(shuffled_cards[i])
	#
	# 	for i in range(10, 15):
	# 		card_state[shuffled_cards[i]] = "P1H"
	#
	# 	for i in range(15, 20):
	# 		card_state[shuffled_cards[i]] = "P2H"
	#
	# 	trump_suit = Deck.get_suit(shuffled_cards[0])
	#
	# 	return Deck(card_state, stock, trump_suit)

	#Look into overloading this function as well
	@staticmethod
	def generate(id):
		if id is 0:
			id = random.randint(0, 100000)

		rng = random.Random(id)
		shuffled_cards = range(20)
		rng.shuffle(shuffled_cards)

		card_state = [0]*20
		stock = [] # Can be thought of as a stack data structure.

		# Three separate for loops assign a state to the cards in the
		# shuffled deck depending on their position. The indices of the
		# stock cards are pushed onto the stock stack to save their order.
		for i in range(10):
			card_state[shuffled_cards[i]] = "S"
			stock.append(shuffled_cards[i])

		for i in range(10, 15):
			card_state[shuffled_cards[i]] = "P1H"

		for i in range(15, 20):
			card_state[shuffled_cards[i]] = "P2H"

		trump_suit = Deck.get_suit(shuffled_cards[0])

		return Deck(card_state, stock, trump_suit)


	def clone(self):
		deck = Deck(list(self.__card_state), list(self.__stock), self.__trump_suit)
		deck.__trick = self.__trick
		return deck

