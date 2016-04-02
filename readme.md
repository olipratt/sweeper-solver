# Sweeper Solver

An automated solver for sweeper games - namely [Mamono Sweeper](http://www.hojamaka.com/game/mamono_sweeper_h_ex/en.html).

## Prerequisites

Requires Python 3.5. No non-default packages.

## Running The Solver

Run `python main.py` in the root of the repository for help, but there are two main modes of operation:

- Automated, e.g. `python main.py -a -d huge-extreme -p 0.1` - run the solver against an internally generated random game and watch its progress. It has to randomly select starting squares to reveal, so might be unlucky and die almost immediately, but after it's revealed a few squares it usually manages to solve the game.

- Interactive, e.g. `python main.py -i` - run interactively, where you provide the game parameters of the game you are playing, and it will give you next moves to make and ask for the results of moves. The idea being you start this alongside a real game, and it helps solve it.

## Interpreting Output

In automated mode, a condensed view of the game board is printed out to make it easier to see the current game state, just showing the level of the enemy on each square or `?` if not revealed yet.

In interactive mode, output looks like a grid of squares represented similar to the following:

    [0-5]?--

- The range in the `[]` shows the solver's knowledge of the possible range of the enemy in that square, which it can slowly make more accurate as the game progresses and more squares are revealed.
- The `?` shows that the square hasn't yet been revealed on the real board, and becomes a `/` once it has.
- The `--` will contain the sum of all neighbouring enemies levels once the square has been revealed and the value has been input.

## Future Improvements

- Running interactively is slow and clunky at best.
    - Ideally it would automatically play the game for you while you watch, but that would probably mean something like platform specific mouse control.
    - Maybe adding a HTTP interface would work, so you could run some javascript in a browser to click?
- Add proper support for plain old minesweeper - might work just by defining a game with life of 1 and all level 1 enemies?

## Running Unit Tests

Run the following from the root of the repository:

    python -m unittest discover
