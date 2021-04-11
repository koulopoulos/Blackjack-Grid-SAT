import numpy as np
from z3 import *
from random import Random


CARD_VALUE = {
    "0": 0, "A": 1, "2": 2, "3": 3, "4": 4, 
    "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, 
    "10": 10, "J": 10, "Q": 10, "K": 10
}

CARD_REPR = {
    0: "0", 1: "A", 2: "2", 3: "3", 4: "4", 
    5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 
    10: "10", 11: "J", 12: "Q", 13: "K"
}


"""
And( # every cell on the board must have a valid state
    Or( # only one card (or no card) can exist in cell (0, 0)
        And(c0_0_0, Not(c_0_0_A), Not(c_0_0_2), ... Not(c_0_0_K)) # no card in cell
        And(Not(c_0_0_0), c_0_0_A, Not(c_0_0_2), ... Not(c_0_0_K)) # ace in cell
        And(Not(c_0_0_0), Not(c_0_0_A), c_0_0_2, ... Not(c_0_0_K)) # 2 in cell
        ...
        And(Not(c_0_0_0), Not(c_0_0_A), Not(c_0_0_2), ... c_0_0_K) # king in cell
    )
    ...
    Or( # only one card (or no card) can exist in cell (5, 5)
        And(c_5_5_0, Not(c_5_5_A), Not(c_5_5_2), ... Not(c_5_5_K)) # no card in cell
        And(Not(c_5_5_0), c_5_5_A, Not(c_5_5_2), ... Not(c_5_5_K)) # ace in cell
        And(Not(c_5_5_0), Not(c_5_5_A), c_5_5_2, ... Not(c_5_5_K)) # 2 in cell
        ...
        And(Not(c_5_5_0), Not(c_5_5_A), Not(c_5_5_2), ... c_5_5_K) # king in cell
    )
)
"""
def board_c(size, n_cards):
    cells_c = []
    for y in range(size):
        for x in range(size):
            cells_c.append(Or(cell_c(x, y, n_cards)))
    return And(cells_c)


"""
Or( # only one card (or no card) can exist in cell (0, 0)
    And(c0_0_0, Not(c_0_0_A), Not(c_0_0_2), ... Not(c_0_0_K)) # no card in cell
    And(Not(c_0_0_0), c_0_0_A, Not(c_0_0_2), ... Not(c_0_0_K)) # ace in cell
    And(Not(c_0_0_0), Not(c_0_0_A), c_0_0_2, ... Not(c_0_0_K)) # 2 in cell
    ...
    And(Not(c_0_0_0), Not(c_0_0_A), Not(c_0_0_2), ... c_0_0_K) # king in cell
)
"""
def cell_c(x, y, n_cards):
    cell_c = []
    for k in range(n_cards + 1):
        card_c = []
        for c in range(n_cards + 1):
            card_c.append(
                Bool(f"c_{x}_{y}_{CARD_REPR[c]}")
                if c == k 
                else Not(Bool(f"c_{x}_{y}_{CARD_REPR[c]}")))
        cell_c.append(And(card_c))
    return cell_c


"""
And(
    Xor(Or(TET CARD ASSIGNMENT), c_0_0_0)),
    Xor(Or(TET CARD ASSIGNMENT), c_1_0_0)),
    ...
    Xor(Or(TET CARD ASSIGNMENT), c_5_5_0)
)
"""
def unassigned_zero_c(size, n_tets, n_cards):
    uz_c = []
    for y in range(size):
        for x in range(size):
            assignments_c = []
            for n in range(n_tets):
                for c in range(1, n_cards + 1):
                    assignments_c.append(Bool(f"tc{n}_{x}_{y}_{CARD_REPR[c]}"))
            uz_c.append(Xor(Or(assignments_c), Bool(f"c_{x}_{y}_0")))
    return And(uz_c)


""" TET

And(
    Or( # tet must assign its cards to some positions
        And(c_0_0_A, c_1_0_A, c_0_1_A, c_1_1_A),
        And(c_1_0_A, c_2_0_A, c_1_1_A, c_2_1_A),
        ...
        And(c_5_5_A, c_6_5_A, c_5_6_A, c_6_6_A),
    )
)

"""
def tet_c(size, n_cards, cards):
    return And(
        Bool("tc0_0_0_A") == True,
        Bool("tc0_1_0_A") == True,
        Bool("tc0_0_1_A") == True,
        Bool("tc0_1_1_A") == True,
        Bool("tc0_0_0_A") == Bool("c_0_0_A"),
        Bool("tc0_1_0_A") == Bool("c_1_0_A"),
        Bool("tc0_0_1_A") == Bool("c_0_1_A"),
        Bool("tc0_1_1_A") == Bool("c_1_1_A")
    )


"""
    [[0, 0, 0, 0, 0, 0]
     [0, 0, 0, 0, 0, 0]
     [0, 0, 0, 0, 0, 0]
     [0, 0, 0, 0, 0, 0]
     [0, 0, 0, 0, 0, 0]
     [0, 0, 0, 0, 0, 0]]
"""
def render_board_model(model, size):
    board = [[0 for _ in range(size)]
                for _ in range(size)]
    for literal in model:
        if m.evaluate(Bool(str(literal))):
            data = str(literal).split("_")
            if data[0] == "c":
                board[int(data[2])][int(data[1])] = data[3]
    print(np.array(board))


if __name__ == "__main__":
    BOARD_SIZE = 6

    s = Solver()
    s.add(And(
        board_c(BOARD_SIZE, 13),
        unassigned_zero_c(BOARD_SIZE, 1, 13),
        tet_c(BOARD_SIZE, 13, ["A", "A", "A", "A"])
    ))

    if s.check() == sat:
        m = s.model()
        render_board_model(m, BOARD_SIZE)
