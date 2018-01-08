Intelligent Systems 2018
========================
This is the practical material for the Intelligent Systems course, based on the
card based strategy game _Schnapsen_.

## Getting started

To get to know the concept of the game, please visit 
[this web page](https://www.pagat.com/marriage/schnaps.html).

Your job is to make a bot that will play this game. 

## Technical requirements

You require a working Python 2.7 environment and a good text editor or an IDE. You can download Python 2.7 for your machine from the following sources:  
* [Windows](https://www.python.org/downloads/windows/)  
* [MacOS](https://www.python.org/downloads/mac-osx/)  
* [Linux](https://www.python.org/downloads/source/)
* [Other](https://www.python.org/download/other/)

### Python knowledge

You will of course also need a working knowledge of python. If you're looking to 
brush up on your skills, there are many good tutorials available. For instance:
 * https://www.learnpython.org/
 * https://www.codecademy.com/ 
 
You do not need to be an expert in python to write a functioning bot. If you
already know another programming language, you should be able to get going within 
a day. You'll pick up the details as the project progresses. However, there are 
a few things that are important to understand. Check if you know what the 
following mean. If not, take some time to google them and read up:

#### Call-by-reference (and "call-by-value")

What happens if I pass a function a 'State' object, and the function changes the
object? Do I keep an unchanged state, or does my state change as well? 

#### Object oriented programming

What's the difference between a class and an object? How are these expressed in python? 
What does the _self_ keyword do?

#### Recursion

Briefly: a method calling itself. Why would this useful, and how does it work?

#### List comprehensions

Advanced python, but they occur occasionally in the code. Useful to know.

## Examples

Here are some quick use cases and solutions to help you get a feel for the code.

### Get the size of the stock
Let 'state' be the state you're given and let's say you want the size of the stock. Then the following a should do the trick:
```python
size_of stock = state.get_stock_size()
```

### Find out if I'm player 1 or 2

```python
me = state.whose_turn()
```

### Print the (abbreviated) cards in your hand

```python
cards_hand = state.hand()

for i, card in enumerate(cards_hand):

	rank, suit = util.get_card_name(card)

	print('Card {} in the hand is {} of {}'.format(i, rank,suit))
```

NB: The deck of cards is represented through an array. Each index corresponds to a different card, as per the table below.

|          | Aces | 10s | Kings | Queens | Jacks |
|:--------:|:----:|:---:|:-----:|:------:|:-----:|
| **Clubs**|   0  |  1  |   2   |    3   |   4   |
|**Diamonds**|   5|  6  |   7   |    8   |   9   |
|**Hearts**|  10  |  11 |   12  |   13   |   14  |
|**Spades**|  15  |  16 |   17  |   18   |   19  |

### Generate a random state
```python
state = State.generate()

# To deterministically generate the same state each time, the generate method can also take a seed, like so:

state = State.generate(25)
# This will always generate the same starting state, to make testing/debugging your bots easier.
```

### Print a representation of the generated state
```python
print state
```
### Get own/opponent's points

```python
me = state.whose_turn()
opponent = util.other(me)

own_points = state.get_points(me)
opponents_points = state.get_points(opponent)
```

## FAQ

### I found a bit that could be implemented much better/more efficiently.

Our main goal was to write code that was easy to read and to understand. To achieve
this, we've made many methods much less efficient than they need to be. This
is especially important for a project like this where many of the students are 
novice programmers. It is also a 
[good principle](https://en.wikipedia.org/wiki/Program_optimization#When_to_optimize) 
in general, at least when you write the first version of your code.

You may feel that your bot is to slow with our State and Fleet objects for 
instance if you're creating an evaluating lots of State objects in a deep
minimax tree. Luckily, you're not tied to our API: simply take the State object 
you're given and copy it to your own, more efficient, implementation. This may 
get you another plie or two in the search tree, so if you really want to win the 
competition it might be worth it.  

### I found a bug/improvement. Can I fork the project and send a pull request?

Sure! Just remember this is not a regular project: we've tried to minimize the 
amount of advanced python, and the number of dependencies. So, it might be that 
we're aware of the potential improvement, but we haven't used it just to keep the 
code simple for novice programmers.  

### The command-line scripts (play.py, tournament.py) make it difficult to do X

The command line scripts provide a convenient starting point, but if you want to do 
something more complex (like try a range of parameters for your bot), they are probably 
too limited. 

Your best bet is to write your own script that does what you want, and have it call the 
engine. Have a look at the function play(...) in  api/engine.py, or have it run a by 
itself. See experiment.py for an example.

## Changes from last year's challenge

The codebase has been rewritten entirely, so bots from last year won't work. This year the game of Schnapsen is being introduced to take the place of Planet Wars.