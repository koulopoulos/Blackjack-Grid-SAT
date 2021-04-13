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



# restrict every board cell between [0, 13]
def cells_c(board, board_size):
    cells_c = []
    for y in range(board_size):
        for x in range(board_size):
            cells_c.append(
                And(0 <= board[y][x], 
                    board[y][x] <= 13))
    return cells_c



# generate tet clauses
def tets_c(tets, board, board_size):
    tets_c = []
    tets_c.append(distinct_c(tets))
    for z in range(len(tets)):
        tets_c.append(tet_c(tets[z], z, board, board_size))
    return And(tets_c)



# generate individual tet clause
def tet_c(tet, z, board, board_size):
    tet_c = []
    # individual card clauses
    for i in range(len(tet)):
        if tet[i] != '0':
            tet_c.append(
                And(range_c(tet[i], z, i, board_size), 
                    assignment_c(tet[i], z, i, board_size)))
    tet_c.append(relative_c(tet, z, board_size))
    return And(tet_c)



# generate card index var
def idx_var(c, z, i):
    return Int(f"{c}.{z}.idx__{i%2}_{i//2}")



# every card index must be distinct
def distinct_c(tets):
    idx_c = []
    for z in range(len(tets)):
        for i in range(len(tets[z])):
            idx_c.append(idx_var(tets[z][i], z, i))
    return Distinct(idx_c)



# card index should be within [0, board_size**2 - 1]
def range_c(rep, z, i, board_size):
    return And(0 <= idx_var(rep, z, i), idx_var(rep, z, i) <= board_size**2 - 1)



# card index implies card value at board index
def assignment_c(rep, z, i, board_size):
    assignment_c = []
    for j in range(board_size**2):
        assignment_c.append(
            Implies(idx_var(rep, z, i) == j, 
                    And(board[j//board_size][j%board_size] == CARD_NUM[rep])))
    return And(assignment_c)



# cards in a tet should be placed relative to each other
def relative_c(tet, z, board_size):
    return And(
            idx_var(tet[0], z, 0) == idx_var(tet[0], z, 1) - 1,
            idx_var(tet[0], z, 0) == idx_var(tet[0], z, 2) - board_size,
            idx_var(tet[0], z, 0) == idx_var(tet[0], z, 3) - board_size - 1)



# clause: a row or column must sum to 21
def blackjack_c(board, board_size, n_tets):
    blackjack_c = []
    for y in range(board_size):
        for x in range(board_size):
            blackjack_c.append(
                Or(sum([board[y][x] for x in range(board_size)]) == 21,
                   sum([board[x][y] for x in range(board_size)]) == 21))
    return Or(blackjack_c)



if __name__ == "__main__":

    # PRIORITY TODO
    # TODO PREVENT ROW WRAPPING
    # TODO DEFAULT CELLS TO 0 IF UNASSIGNED
    # TODO FACE CARDS SHOULD BE VALUED AT 10
    # TODO RUNS FOREVER WITH 9 SQUARE TETS

    BOARD_SIZE = 6

    tets = []
    print("Input the number of tets for the game:")
    n = int(input())
    for _ in range(n):
        tets.append(str(input()))
    
    start = timeit.default_timer()

    board = [[Int(f"b_{x}_{y}") for x in range(BOARD_SIZE)]
                                for y in range(BOARD_SIZE)]

    s = Solver()
    s.add(cells_c(board, BOARD_SIZE))
    s.add(tets_c(tets, board, BOARD_SIZE))
    #s.add(blackjack_c(board, BOARD_SIZE, len(tets)))

    if s.check() == sat:
        stop = timeit.default_timer()
        m = s.model()
        print(np.array(
            [[CARD_REPR[m.evaluate(board[y][x]).as_long()] 
                for x in range(BOARD_SIZE)]
                for y in range(BOARD_SIZE)]))
        print(f"Runtime: {stop - start}s")
