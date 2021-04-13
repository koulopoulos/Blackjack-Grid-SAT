import numpy as np
from z3 import *
from random import Random

CARD_VAL = {
    0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 
    5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 
    10: 10, 11: 10, 12: 10, 13: 10
}

CARD_REPR = {
    0: "0", 1: "A", 2: "2", 3: "3", 4: "4", 
    5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 
    10: "X", 11: "J", 12: "Q", 13: "K"
}

CARD_NUM = {
    "0": 0, "A": 1, "2": 2, "3": 3, "4": 4, 
    "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, 
    "X": 10, "J": 11, "Q": 12, "K": 13
}


# restrict every board cell between [0, 13]
def cells_c(board, board_size, n_tets):
    cells_c = []
    for y in range(board_size):
        for x in range(board_size):
            for z in range(n_tets):
                cells_c.append(And(0 <= board[z][y][x], board[z][y][x] <= 10))
    return cells_c


# parse user input as tet (card) vars
def tets_c(tets, board, board_size):
    tets_c = []
    for z in range(len(tets)):
        tets_c.append(tet_c(tets[z], z, board, board_size))
    return And(tets_c)


# only one card can exist in one cell
def distinct_c():
    distinct_c = []
    for z in range(len(tets)):
        for i in range(len(tets[z])):
            cx = f"{tets[z][i]}.{z}.x__{i%2}_{i//2}" # repr.z.x__dx_dy
            cy = f"{tets[z][i]}.{z}.y__{i%2}_{i//2}" # repr.z.y__dx_dy


# clause: every card in a tet must have a valid (x,y) location on the board
#           a valid (x, y) implies the card value should be located at that location
#           all cards in a tet are placed relative to each other
def tet_c(tet, z, board, board_size):
    t_c = []

    # individual card clauses
    for i in range(len(tet)):
        if tet[i] != '0':
            card_c = []

            cx = f"{tet[i]}.{z}.x__{i%2}_{i//2}" # repr.z.x__dx_dy
            cy = f"{tet[i]}.{z}.y__{i%2}_{i//2}" # repr.z.y__dx_dy
            
            # card x-value should be within [0, 5]
            card_c.append(And(0 <= Int(cx), Int(cx) <= board_size - 1))
            # card y-value should be within [0, 5]
            card_c.append(And(0 <= Int(cy), Int(cy) <= board_size - 1))

            # link card (x, y) to board (x, y)
            for y in range(board_size):
                for x in range(board_size):
                    card_c.append(
                        Implies(
                            And(Int(cx) == x, Int(cy) == y),
                            And(board[z][y][x] == CARD_NUM[tet[i]])))
                                
            t_c.append(And(card_c))

    # TODO generate this dynamically
    t_c.append(
        And(# associated cards should be place relatively
            Int(f"{tet[0]}.{z}.x__0_0") == Int(f"{tet[1]}.{z}.x__1_0") - 1,
            Int(f"{tet[0]}.{z}.y__0_0") == Int(f"{tet[1]}.{z}.y__1_0"),
            Int(f"{tet[0]}.{z}.x__0_0") == Int(f"{tet[2]}.{z}.x__0_1"),
            Int(f"{tet[0]}.{z}.y__0_0") == Int(f"{tet[2]}.{z}.y__0_1") - 1,
            Int(f"{tet[0]}.{z}.x__0_0") == Int(f"{tet[3]}.{z}.x__1_1") - 1,
            Int(f"{tet[0]}.{z}.y__0_0") == Int(f"{tet[3]}.{z}.y__1_1") - 1,
        ))

    return And(t_c)


# clause: there cannot exist a collision between tets in the z-index
def collision_c(board, len_board, n_tets):
    collision_c = []
    for y in range(len_board):
        for x in range(len_board):
            for tz in range(n_tets):
                for z in range(n_tets):
                    if tz != z:
                        collision_c.append(Implies(board[tz][y][x] != 0, board[z][y][x] == 0))
    return And(collision_c)


# clause: a row or column must sum to 21
def blackjack_c(board, board_size, n_tets):
    blackjack_c = []
    for z in range(n_tets):
        for y in range(board_size):
            blackjack_c.append(Or(
                sum([board[z][y][x] for x in range(board_size)]) == 21,
                sum([board[z][x][y] for x in range(board_size)]) == 21
            ))
    return Or(blackjack_c)


if __name__ == "__main__":
    BOARD_SIZE = 6

    tets = []
    print("Input the number of tets for the game:")
    n = int(input())
    for _ in range(n):
        tets.append(str(input()))

    board = [[[Int(f"b_{x}_{y}_{z}") for x in range(BOARD_SIZE)]
                                     for y in range(BOARD_SIZE)]
                                     for z in range(len(tets))]

    s = Solver()
    s.add(cells_c(board, BOARD_SIZE, len(tets)))
    s.add(tets_c(tets, board, BOARD_SIZE))
    s.add(collision_c(board, BOARD_SIZE, len(tets)))
    s.add(blackjack_c(board, BOARD_SIZE, len(tets)))

    if s.check() == sat:
        m = s.model()
        board_repr = []

        for y in range(BOARD_SIZE):
            row = []
            for x in range(BOARD_SIZE):
                row.append(CARD_REPR[sum([m.evaluate(board[z][y][x]).as_long() 
                                        for z in range(len(tets))])])
            board_repr.append(row)

        print(np.array(board_repr))



# DONE?
# TODO collision detection
# TODO 'ghost cards'

# NOT DONE
# TODO infinite loop / not running with 9 tets
# TODO face cards should be 10
# TODO default empty cells to 0 if not assigned

