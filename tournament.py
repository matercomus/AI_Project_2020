#!usr/bin/env python
"""
A command line program for multiple games between several bots.

For all the options run
python play.py -h
"""

from argparse import ArgumentParser
from api import State, util, engine
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind


def run_tournament(options):

    botnames = options.players.split(",")

    bots = []
    for botname in botnames:
        bots.append(util.load_player(botname))

    n = len(bots)
    wins = [0] * len(bots)
    matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

    totalgames = (n*n - n)/2 * options.repeats
    playedgames = 0
    score_list_p1 = []
    score_list_p2 = []
    print('Playing {} games:'.format(int(totalgames)))
    for a, b in matches:
        for r in range(options.repeats):

            if random.choice([True, False]):
                p = [a, b]
            else:
                p = [b, a]

            # Generate a state with a random seed
            state = State.generate(phase=int(options.phase))

            winner, score = engine.play(
                bots[p[0]], bots[p[1]], state, options.max_time*1000, verbose=False, fast=options.fast)

            if winner is not None:
                winner = p[winner - 1]
                wins[winner] += score

            playedgames += 1

            for index, value in enumerate(wins):
                if index % 2 != 0:
                    score_list_p2.append(value)
                else:
                    score_list_p1.append(value)

            print('Played {} out of {:.0f} games ({:.0f}%): {} \r'.format(
                playedgames, totalgames, playedgames/float(totalgames) * 100, wins))

    print('Results:')
    for i in range(len(bots)):
        print('    bot {}: {} points'.format(bots[i], wins[i]))

    # print('p1: {}'.format(score_list_p1))
    # print('p2: {}'.format(score_list_p2))
    score_list_p1_p2 = list(zip(score_list_p1, score_list_p2))
    # print(score_list_p1_p2)

    scores_data = pd.DataFrame(score_list_p1_p2, columns=[
        'Player 1 score', 'Player 2 score'])

    # Calculate the T-test for the means of two independent samples of scores.
    ttest_result = ttest_ind(scores_data['Player 1 score'],
                             scores_data['Player 2 score'])

    print(ttest_result)

    # print(scores_data)

    plt.title(
        'Tournament score of both bots')
    plt.plot(scores_data.index,
             scores_data['Player 1 score'], marker='.', label=botnames[0])
    plt.plot(scores_data.index,
             scores_data['Player 2 score'], marker='.', label=botnames[1])

    plt.xlabel('Game #')
    plt.ylabel('Score')
    plt.legend()
    plt.savefig('plot')
    plt.show()


if __name__ == "__main__":

    # Parse the command line options
    parser = ArgumentParser()

    parser.add_argument("-s", "--starting-phase",
                        dest="phase",
                        help="Which phase the game should start at.",
                        default=1)

    parser.add_argument("-p", "--players",
                        dest="players",
                        help="Comma-separated list of player names (enclose with quotes).",
                        default="rand,bully,rdeep")

    parser.add_argument("-r", "--repeats",
                        dest="repeats",
                        help="How many matches to play for each pair of bots",
                        type=int, default=10)

    parser.add_argument("-t", "--max-time",
                        dest="max_time",
                        help="maximum amount of time allowed per turn in seconds (default: 5)",
                        type=int, default=5)

    parser.add_argument("-f", "--fast",
                        dest="fast",
                        action="store_true",
                        help="This option forgoes the engine's check of whether a bot is able to make a decision in the allotted time, so only use this option if you are sure that your bot is stable.")

    options = parser.parse_args()

    run_tournament(options)
