Intelligent Systems 2017
========================
This is the practical material for the Intelligent Systems course, based on the
card based strategy game _Schnapsen_.

## Getting started

To get to know the concept of the game, please visit 
[this web page](https://www.pagat.com/marriage/schnaps.html).

Your job is to make a bot that will play this game. 

## Technical requirements

You require a working python 2.7 environment and a good text editor or an IDE. If 
that's enough information, read on below. If you're not quite sure how to go
about this, see the installation tutorial on Blackboard. There will be a hands-on
session in the first week to help you get started. 

## The rules of planetwars

The rules are encoded in the engine, spefically in the methods moves() and next() 
of the [state object](https://github.com/intelligent-systems-course/planet-wars/blob/master/api/_state.py).

Here's a quick summary:

 * The aim of the game is to eradicate all planets and ships of the opposing player.
 * The two players move one at a time.
 * A move is made by sending ships from one planet (the source) to another (the destination).
 * A move always results in half the source planet's ships travelling towards the destination.
 * A collection of ships in transit is called a _fleet_.
 * If, on arrival, the target planet is _neutral_ (not owned by any player) or owned by the opponent, the fleet attacks the planet: one ship in the fleet cancels out against one ship on the planet. If the fleet has ships left over and the planet doesn't, the fleet's owner takes over ownership of the planet, and the remainder of the fleet becomes stationed at the planet.
 * If, on arrival, the target planet is owned by the owner of the fleet, the fleet reinforces the planet: the ships in the fleet are added to those already at the planet.
 * Planets occasionally produce ships; the bigger the planet the faster they produce ships. A planet of size 1/n, produces a ship every n turns. The biggest planet size is 1, which produces a ship every turn.
 * The standard playing field has size planets. Each player starts with one planet of size 1, at opposite corners of the playing field, cotaining 100 ships. The other four planets are distributed randomly. For the generating code, look at the function [State.generate](https://github.com/intelligent-systems-course/planet-wars/blob/master/api/_state.py#L440)

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

### Get the size of a planet
Let 'state' be the state you're given and let's say you want the size of the i'th planet. Then the following a should do the trick:
```python
size_of planet_i = state.planets()[i].size()
```
Or, to print the size of every planet:
```python
for planet in state.planets():
    print 'planet {} has size {}.'.format(planet.id(), planet.size())
```

### Find out if I'm player 1 or 2

```python
me = state.whose_turn()
```

### Print the coordinates of all fleets source and target planet

```python
for i, fleet in enumerate(state.fleets()):

    source = fleet.source()
    target = fleet.target()
    
    source_crds = source.coords()
    target crds = target.coords()
    
    print('Fleet {} is moving from {} to {}'.format(i, source_crds, target_crds))
```

### Draw a PNG of a single state
```python
fig = state.visualize()   # this is a matplotlib Figure object
fig.savefig('state.png')  # matplotlib detects the format you want from the extension you use
```

### Generate a random state
```python
rand_state = State.generate()
```
### Compute the average number of ships on one of my planets

```python
me = state.whose_turn()
my_planets = state.planets(me)

avg = 0.0
for planet in my_planets:
    avg += state.garrison(planet)

avg = avg / len(my_planets)

print('average ships per planet: {}'.format(avg))
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

The codebase has been rewritten entirely, so bots from last year won't work. To
reduce overhead, Java is no longer supported, only python.
