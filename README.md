# Blackjack Grid Solver

## Introduction 
In Blackjack Grid, a player places tetromino-like clusters of traditional playing cards, which we refer to as "card-tets" or "tets", within a 6x6 grid. The objective of the game is to place cards such that the sum of their values is 21 in either a row or column of the board. If there is no space remaining on the board to fit the next card-tet, then the game is over. Although the original game clears all cards in a given row or column once they sum to 21, an aspect which introduces discrete "time frames" in the form of board states, our solver considers only a single board frame where the player has *N* card-tets to place.

```
[0, 0, 0, 5, 0, 0]
[0, A, Q, 0, 3, 3]

    [A, 3, 0, 0, 7, J] = 21

[0, 0, 0, 0, 0, 0]
[0, 0, 0, K, 6, 0]
[0, X, 0, 0, 4, 0]
              
```

## Project Structure
```
| solver
  | src 
    | __init__.py 
    | solver.py
  | tests 
    | __init__.py
  | .gitignore
  | README.md
  | requirements.txt
```

## Setup
1. Install python dependencies
    * `pip install -r requirements.txt`
2. Run the solver
    * `python src/solver.py`

## Example Usage
```
Blackjack Grid Solver
> Input the board size: 6
> Input the tets as CSV: AAA0, K452, 0077, 0984, 450Q, JJJ3

[['0' '0' '0' '0' '0' '9']
 ['0' 'K' '4' '0' '8' '4']
 ['0' '5' '2' '7' '7' '0']
 ['0' 'J' 'J' '0' '4' '5']
 ['0' 'J' '3' 'A' 'A' 'Q']
 ['0' '0' '0' 'A' '0' '0']]

Runtime: 0.15606081700000374s
```

## References
1. https://play.gamezop.com/p/gamepage/SyIZjp3GulZ
