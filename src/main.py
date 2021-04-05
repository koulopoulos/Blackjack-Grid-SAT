import numpy as np
from random import Random


def cell_literals():
    board = []
    for i in range(6):
        for j in range(6):
            cell = []
            for c in range(1, 14):
                cell.append((str(i) + str(j) + str(c).zfill(2) , False))
            board.append(cell)
    return board


def card_tet():
    tet = []
    for i in range(2):
        for j in range(2):
            cell = []
            for c in range(1, 14):
                cell.append((str(i) + str(j) + str(c).zfill(2) , False))
            tet.append(cell)
    return tet


def shuffle_tet(tet, rand):
    indices = rand.sample([0, 1, 2, 3], rand.randint(1, 4))
    for index in indices:
        r = rand.randint(0,12)
        tet[index][r] = (tet[index][r][0], True)
    return tet


if __name__ == "__main__":
    print(np.array([shuffle_tet(card_tet(), Random(1))]))
