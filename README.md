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
> Input the board size:
> 6

> Input the number of tets for the game:
> 2

> Input the tets (Use 0 for no card and X for 10)
> AAAA
> K900

> [['0' '0' '0' '0' '0' '0']
>  ['0' '0' 'A' 'A' '0' '0']
>  ['K' '9' 'A' 'A' '0' '0']
>  ['0' '0' '0' '0' '0' '0']
>  ['0' '0' '0' '0' '0' '0']
>  ['0' '0' '0' '0' '0' '0']]
```

## Known Bugs
* ~~Card-tets can wrap across one edge of the board to the other.~~
* ~~Cells are not restricted to 0 if unassigned by a tet.~~
* ~~The Blackjack clause uses the card ID instead of value.~~

## References
1. https://play.gamezop.com/p/gamepage/SyIZjp3GulZ
