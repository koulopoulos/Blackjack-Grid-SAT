import numpy as np
from z3 import *


def make_tets(n, shapes, cards, rand):
    """Generates N 2x2 card-tets

        Args:
            n: the number of card-tets to generate
            shapes: a list of card-tet shapes to choose from
            cards: the list of playing cards to choose from
            rand: the random object for generation

        Returns:
            tets: the list of generated card-tets
    """
    tets = []
    for k in range(n):
        tet = [[0, 0], 
               [0, 0]]
        for posn in shapes[rand.randint(0, len(shapes) - 1)]:    
            tet[posn[0]][posn[1]] = rand.choice(cards)
        tets.append(tet)
    return tets


def board(size):
    """Creates a 2d list which rep. a board with Int z3 vars

        Args:
            size: the n x n dimensions for the list

        Returns:
            board_vars: the 2d list with cell_x_y vars rep. Int z3 values
    """
    board_vars = []
    for y in range(size):
        row = []
        for x in range(size):
            row.append(Int(f"cell_{x}_{y}"))
        board_vars.append(row)
    return board_vars


def cells_c(board_vars):
    """Generates clauses to restrict every cells value in range [0, 10]

        Args:
            board_vars: the Z3 variables representing the board

        Returns:
            the list of clauses
    """
    clause = []
    for y in range(len(board_vars)):
        for x in range(len(board_vars)):
            clause.append(And(0 <= board_vars[y][x], board_vars[y][x] <= 10))
    return clause


def blackjack_c(board_vars):
    """Creates clause that rep. whether a row or column sums to 21

        Args:
            board_vars: rep a list of z3 vars

        Returns:
            A list of clauses that rep. whether a row or column sums to 21
    """
    return [Or(Or([Sum(row) == 21 for row in board_vars]), 
               Or([Sum(col) == 21 for col in np.transpose(board_vars).tolist()]))]


# how do we determine where a tet can not be placed?

# x < 0 || 5 < x
# y < 0 || 5 < y

# how do we determine if this tet is colliding with another?

# placements of tets (all configuration of each tet)
# every piece must exist in only a single location (Distinct) 
# every piece must have a placement 
# sum of rows / columns
# tet collision

# card tet class????

#   [][][][][][]
#   [][][][][][]
#   [][][][][][]
#   [][][][][][]
#   [][][][][][]
#   [][][][][][]


#cX rep a cell
if __name__ == "__main__":
    s = Solver()
    s.add()

    while s.check() == sat:
        m = s.model ()
        print(m)