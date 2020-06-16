"""
SmartRand -- A modified version of rand bot by Matt Kedzia and ...
"""

# Import the API objects
from api import State, util, Deck

import random


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.
        Be sure to make a legal move. Illegal moves, like giving an index of a card you
        don't own or proposing an illegal mariage, will lose you the game.
        TODO: add some more explanation
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """

        # All legal moves
        moves = state.moves()

        # Heuristic 1 - if possible, play a mariage.
        for move in moves:
            if move[1] != None:
                if util.get_suit(move[1]) == state.get_trump_suit():
                    return move
                else:
                    return move

        # Heuristic 2 - if only 1 spouse in hand (and it's partner has not yet been played),
        # don't play it and keep it. Unless it's the only card in hand.
        # TODO: check for partners that were alredy played.

        # check if not the only card in hand
        if len(moves) > 1:
            for move in enumerate(moves):
                # remove single spouses (Kings and Queens) from moves.
                if move[1][0] in (2, 7, 12, 17, 3, 8, 13, 18):
                    moves.pop(move[0])

        # Return a random choice
        return random.choice(moves)
