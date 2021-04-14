import numpy as np
from z3 import *
from random import Random
import timeit

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


# generates the board cell vars
def board_v(board_size):
    return [Int(f"b_{i}") for i in range(board_size**2)]


# generates a card index var
def card_v(c, z, i):
    return Int(f"{c}.{z}.idx__{i%2}_{i//2}")


# restrict every board cell between [0, 13]
def board_c(board, board_size):
    return [And(0 <= board[i], board[i] <= 13) for i in range(board_size**2)]


# generates tet clauses
def tets_c(tets, board, board_size):
    return And([tet_c(tets[z], z, board, board_size) for z in range(len(tets))])


# generates an individual tet clause
def tet_c(tet, z, board, board_size):
    c = []
    for i in range(len(tet)):
        if tet[i] != '0':
            c.append(range_c(tet[i], z, i, board_size))
            c.append(assignment_c(tet[i], z, i, board_size))
    c.append(relative_c(board, board_size, tet, z))
    return And(c)


# every card index must be distinct
def distinct_index_c(tets):
    c = []
    for z in range(len(tets)):
        for i in range(len(tets[z])):
            c.append(card_v(tets[z][i], z, i))
    return Distinct(c)


# card index should be within [0, len(board)**2 - 1]
def range_c(rep, z, i, board_size):
    return And(0 <= card_v(rep, z, i), card_v(rep, z, i) <= board_size**2 - 1)


# card index implies card value at board index
def assignment_c(rep, z, i, board_size):
    return And([Implies(card_v(rep, z, i) == j, board[j] == CARD_NUM[rep])
                    for j in range(board_size**2)])


# cards in a tet should be placed relative to each other
def relative_c(board, board_size, tet, z):
    return And(card_v(tet[0], z, 0) == card_v(tet[1], z, 1) - 1,
               card_v(tet[0], z, 0) == card_v(tet[2], z, 2) - board_size,
               card_v(tet[0], z, 0) == card_v(tet[3], z, 3) - board_size - 1)


# clause: a row or column must sum to 21
def blackjack_c(board, board_size):
    c = []
    for i in range(board_size):
        c.append(
            Or(sum([board[i+board_size*j] for j in range(board_size)]) == 21,
               sum([board[i*board_size+j] for j in range(board_size)]) == 21))
    return Or(c)


# renders the board to the console
def render_board(board):
    print(np.array(
        [[CARD_REPR[m.evaluate(board[i+j*board_size]).as_long()]
            for i in range(board_size)]
            for j in range(board_size)]))


# receives user input for the board size and tets
def input_tets():
    tets = []
    print("Input the board size:")
    board_size = int(input())
    print("Input the number of tets for the game:")
    n_tets = int(input())
    print("Input the tets (Use 0 for no card and X for 10)")
    for _ in range(n_tets):
        tets.append(str(input()))
    return board_size, n_tets, tets


if __name__ == "__main__":

    # get user input
    board_size, n_tets, tets = input_tets()

    # setup board 
    board = board_v(board_size)

    # add clauses to solver
    s = Solver()
    s.add(board_c(board, board_size))
    s.add(tets_c(tets, board, board_size))
    s.add(distinct_index_c(tets))
    s.add(blackjack_c(board, board_size))

    # solve
    start = timeit.default_timer()
    if s.check() == sat:
        stop = timeit.default_timer()
        m = s.model()
        render_board(board)
        print(f"Runtime: {stop - start}s")
