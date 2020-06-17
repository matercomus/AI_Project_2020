"""
SmartRand -- A modified version of rand bot by Matt Kedzia and ...
"""

# Import the API objects
from api import State, util, Deck

import random


class Bot:

    def __init__(eck):
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
            if move[1] != None and move[1] != None:
                if util.get_suit(move[1]) == state.get_trump_suit():
                    return move
                else:
                    return move

        # Heuristic 2 - if only 1 spouse in hand (and it's partner has not been played in the previous trick),
        # don't play it and keep it. Unless it's the only card in hand.
        # TODO: check for partners that were played in previous trick.

        # check if not the only card in hand
        prev_trick = state.get_prev_trick()
        if len(moves) > 1:
            for move in enumerate(moves):
                # remove single spouses (Kings and Queens) from moves if their partners were played in the previous trick.
                if move[1][0] in (2, 7, 12, 17):    # test if King
                    if prev_trick[0] not in (3, 8, 13, 18):
                        pass  # if card 1 from previous trick is not a queen, pass
                    if prev_trick[1] not in (3, 8, 13, 18):
                        pass  # if card 2 from previous trick is not a queen, pass
                    else:
                        # spouse detected in previous trick, remove from moves.
                        moves.pop(move[0])
                        print(
                            'removed move {}, single spouse detected.'.format(move[1]))
                        print('previous trick --> {}'.format(prev_trick))
                elif move[1][0] in (3, 8, 13, 18):  # test if queen
                    if prev_trick[0] not in (2, 7, 12, 17):
                        pass  # if card 1 from previous trick is not a king, pass
                    if prev_trick[1] not in (2, 7, 12, 17):
                        pass  # if card 2 from previous trick is not a king, pass
                    else:
                        # spouse detected in previous trick, remove from moves.
                        moves.pop(move[0])
                        print(
                            'removed move {}, single spouse detected.'.format(move[1]))
                        print('previous trick --> {}'.format(prev_trick))

        # TESTS
        # print('TESTS:')

        # perspective
        # perspective = state.get_perspective(state.whose_turn())
        # print(perspective)

        # print('previous trick --> {}'.format(prev_trick))
        # print(prev_trick[0], prev_trick[1])

        # //TESTS END//
        # Return a random choice
        return random.choice(moves)
