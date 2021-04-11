import numpy as np
from z3 import *
from random import Random

CARD_VALUE = {
    0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 
    5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 
    10: 10, 11: 10, 12: 10, 13: 10
}

CARD_REPR = {
    0: "0", 1: "A", 2: "2", 3: "3", 4: "4", 
    5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 
    10: "10", 11: "J", 12: "Q", 13: "K"
}

CARD_VAL = {
    "0": 0, "A": 1, "2": 2, "3": 3, "4": 4, 
    "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, 
    "10": 10, "J": 11, "Q": 12, "K": 13
}


def cells_c(board):
    cells_c = []
    for x in range(len(board)):
        for y in range(len(board)):
            cells_c.append(And(0 <= board[x][y], board[x][y] <= 13))
    return cells_c


def parse_tets(tets):
    parsed = []
    for z in range(len(tets)):
        parsed.append(tet_c(tets[z], z))
    return parsed


def tet_c(tet, z):
    tet_p = []
    tet_b = []
    for i in range(len(tet)):
        tet_p.append(
                (Int(f"{CARD_VAL[tet[i]]}.{z}__{i%2}_{i//2}_x"), 
                 Int(f"{CARD_VAL[tet[i]]}.{z}__{i%2}_{i//2}_y")))
    return tet_p
    
And(
    Int(1.0__0_0_x) == Int(1.0__1_0_x) + 1
    Int(1.0__0_0_y) == Int(1.0__1_0_y)

    Int(1.0__0_0_x) == Int(1.0__0_1_x)
    Int(1.0__0_0_y) == Int(1.0__0_1_y) + 1

    Int(1.0__0_0_x) == Int(1.0__1_1_x) + 1
    Int(1.0__0_0_y) == Int(1.0__1_1_y) + 1
)

def inbounds_c():
    pass

#AAAA 0 (0,0) 1 (0,1) 2 (1,0) 3 (1,1)

if __name__ == "__main__":
    tets = []
    print("Input the number of tets for the game:")
    n = int(input())
    for _ in range(n):
        tets.append(str(input()))
    print(np.array(parse_tets(tets)))












"""
def blackjack_c(board):
    blackjack_c = []
    for x in range(len(board)):
        for y in range(len(board)):
            Or([Sum([CARD_VALUE[c] for c in row]) == 21 for row in board]), 
            Or([Sum(col) == 21 for col in np.transpose(board).tolist()]))

board = [[Int(f"c_{x}_{y}") for x in range(6)]
                            for y in range(6)]

s = Solver()
s.add(cells_c(board))

if s.check() == sat:
    m = s.model()
    print(np.array([ [ m.evaluate(board[i][j]) for j in range(6) ]
        for i in range(6) ]))
"""