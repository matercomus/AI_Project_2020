#!/usr/bin/env python
"""
A basic adaptive bot. This is part of the third worksheet.

"""

from api import State, util
import random, os

from sklearn.externals import joblib

# Path of the model we will use. If you make a model
# with a different name, point this line to its path.
DEFAULT_MODEL = os.path.dirname(os.path.realpath(__file__)) + '/model.pkl'

class Bot:

    __randomize = True

    __model = None

    def __init__(self, randomize=True, model_file=DEFAULT_MODEL):

        print(model_file)
        self.__randomize = randomize

        # Load the model
        self.__model = joblib.load(model_file)

    def get_move(self, state):

        val, move = self.value(state)

        return move

    def value(self, state):
        """
        Return the value of this state and the associated move
        :param state:
        :return: val, move: the value of the state, and the best move.
        """

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        for move in moves:

            next_state = state.next(move)

            # IMPLEMENT: Add a function call so that 'value' will
            # contain the predicted value of 'next_state'
            # NOTE: This is different from the line in the minimax/alphabeta bot
            value = ???

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        return best_value, best_move

    def heuristic(self, state):

        # Convert the state to a feature vector
        feature_vector = [features(state)]

        # These are the classes: ('won', 'lost')
        classes = list(self.__model.classes_)

        # Ask the model for a prediction
        # This returns a probability for each class
        prob = self.__model.predict_proba(feature_vector)[0]

        # Weigh the win/loss outcomes (-1 and 1) by their probabilities
        res = -1.0 * prob[classes.index('lost')] + 1.0 * prob[classes.index('won')]

        return res

def maximizing(state):
    """
    Whether we're the maximizing player (1) or the minimizing player (2).
    :param state:
    :return:
    """
    return state.whose_turn() == 1


def features(state):
    # type: (State) -> tuple[float, ...]
    """
    Extract features from this state. Remember that every feature vector returned should have the same length.

    :param state: A state to be converted to a feature vector
    :return: A tuple of floats: a feature vector representing this state.
    """

    feature_set = []

    perspective = state.get_perspective()

    # Convert the card state array containing strings, to an array of integers.
    # The integers here just represent card state IDs. In a way they can be
    # thought of as arbitrary, as long as they are different from each other.
    perspective = [card if card != 'U' else (-1) for card in perspective]
    perspective = [card if card != 'S' else 0 for card in perspective]
    perspective = [card if card != 'P1H' else 1 for card in perspective]
    perspective = [card if card != 'P2H' else 2 for card in perspective]
    perspective = [card if card != 'P1W' else 3 for card in perspective]
    perspective = [card if card != 'P2W' else 4 for card in perspective]

    feature_set += perspective

    # Add player 1's points to feature set
    p1_points = ???
    feature_set.append(p1_points)

    # Add player 2's points to feature set
    p2_points = ???
    feature_set.append(p2_points)

    # Add player 1's pending points to feature set
    p1_pending_points = ???
    feature_set.append(p1_pending_points)

    # Add plauer 2's pending points to feature set
    p2_pending_points = ???
    feature_set.append(p2_pending_points)

    # Get trump suit
    trump_suit = ???

    # Convert trump suit to id and add to feature set
    # You don't need to add anything to this part
    suits = ["C", "D", "H", "S"]
    trump_suit_id = suits.index(trump_suit)
    feature_set.append(trump_suit_id)

    # Add phase to feature set
    phase = ???
    feature_set.append(phase)

    # Add stock size to feature set
    stock_size = ???
    feature_set.append(stock_size)

    # Add leader to feature set
    leader = ???
    feature_set.append(leader)

    # Add whose turn it is to feature set
    whose_turn = ???
    feature_set.append(whose_turn)

    # Add opponent's played card to feature set
    opponents_played_card = ???

    # You don't need to add anything to this part
    opponents_played_card = opponents_played_card if opponents_played_card is not None else -1
    feature_set.append(opponents_played_card)

    # Return feature set
    return feature_set
