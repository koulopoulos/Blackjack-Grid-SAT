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


def board_v(board_size):
    """ Generates Z3 variables to represent the board cells

        Args:
            board_size: the side length of the board (in cells)

        Returns:
            A list of Z3 integer variables
    """
    return [Int(f"b_{i}") for i in range(board_size**2)]


def card_v(rep, z, i):
    """ Generates a single Z3 variable representing a card index

        Args:
            rep: the character representation of the card
            z: the identifier of the Tet the card belongs to
            i: the card's indexed location relative to its Tet

        Returns:
            A Z3 integer variable
    """
    return Int(f"{rep}.{z}.idx__{i%2}_{i//2}")


def board_c(board, board_size):
    """ Builds a Z3 clause which restricts the range of every board
        cell variable, such that they can only hold a valid card ID.

        Args:
            board: a list of Z3 integer variables representing the board cells
            board_size: the side length of the board (in cells)

        Returns:
            A list of Z3 conjunctive clauses
    """
    return [And(0 <= board[i], board[i] <= 13) for i in range(board_size**2)]


def tets_c(tets, board, board_size):
    """ Builds a Z3 clause consisting of the Z3 clauses for the given Tets

        Args:
            tets: a list of Tets represented as strings
            board: a list of Z3 integer variables representing the board cells
            board_size: the side length of the board (in cells) 

        Returns:
            A Z3 conjunction of every individual Tet clause
    """
    return And([tet_c(tets[z], z, board, board_size) for z in range(len(tets))])


def tet_c(tet, z, board, board_size):
    """ Builds a Z3 clause consisting of Z3 clauses for each card in the Tet.

        Args:
            tet: a string representation of a Tet
            z: the unique identifier integer for the Tet
            board: a list of Z3 integer variables representing the board cells
            board_size: the side length of the board (in cells) 

        Returns:
            A Z3 conjunction of the clauses generated for each card in the Tet
    """
    c = []
    for i in range(len(tet)):
        if tet[i] != '0':
            c.append(range_c(tet[i], z, i, board_size))
            c.append(assignment_c(tet[i], z, i, board, board_size))
    c.append(relative_c(board_size, tet, z))
    return And(c)


def distinct_index_c(tets):
    """ Builds a Z3 clause which requires all card variables to have a distinct value

        Args:
            tets: a list of Tets represented as strings

        Returns:
            A Z3 Distinct clause 
    """
    c = []
    for z in range(len(tets)):
        for i in range(len(tets[z])):
            if tets[z][i] != '0':
                c.append(card_v(tets[z][i], z, i))
    return Distinct(c)


def range_c(rep, z, i, board_size):
    """ Builds a Z3 clause which restricts a card variable to have a valid board index

        Args:
            rep: the character representation of the card
            z: the identifier of the Tet the card belongs to
            i: the card's indexed location relative to its Tet
            board_size: the side length of the board (in cells)

        Returns:
            A Z3 conjunctive clause
    """
    return And(0 <= card_v(rep, z, i), card_v(rep, z, i) <= board_size**2 - 1)


# card index implies card value at board index
def assignment_c(rep, z, i, board, board_size):
    """ Builds a Z3 clause which 
    """
    return And([Implies(card_v(rep, z, i) == j, board[j] == CARD_NUM[rep])
                    for j in range(board_size**2)])


def default_zero_c(tets, board):
    c = []
    for j in range(board_size**2):
        cell = []
        for z in range(len(tets)):
            for i in range(len(tets[z])):
                if tets[z][i] != '0':
                    cell.append(card_v(tets[z][i], z, i) == j)
        c.append(Implies(Not(Or(cell)), (board[j] == 0)))
    return And(c)
                    

def relative_c(board_size, tet, z):
    """ Builds a Z3 clause which restricts all cards in the Tet to be placed relative to each other

        Args:
            board_size: the side length of the board (in cells)
            tet: a string representation of the Tet
            z: the unique identifier integer for the Tet 

        Returns:
            A Z3 conjunctive clause
    """
    c = []
    
    if (tet[0] != '0' or tet[2] != '0') and (tet[1] != '0' or tet[3] != '0'):
        # restrict to single row please help
        c.append(Not(Or(card_v(tet[1], z, 1) % board_size == 0, 
                        card_v(tet[3], z, 1) % board_size == 0)))

    c.append(card_v(tet[0], z, 0) == card_v(tet[1], z, 1) - 1)
    c.append(card_v(tet[0], z, 0) == card_v(tet[2], z, 2) - board_size)
    c.append(card_v(tet[0], z, 0) == card_v(tet[3], z, 3) - board_size - 1)

    return And(c)
        


# clause: a row or column must sum to 21
def blackjack_c(board, board_size):
    c = []
    for i in range(board_size):
        c.append(
            Or(sum([If(board[i+board_size*j] > 10, 10, board[i+board_size*j]) for j in range(board_size)]) == 21,
               sum([If(board[i*board_size+j] > 10, 10, board[i*board_size+j]) for j in range(board_size)]) == 21))
    return Or(c)


def render_board(board):
    """ Renders the given board to the console

        Args:
            board: the list of Z3 cell variables representing the board

        Return: None
    """
    print(np.array(
        [[CARD_REPR[m.evaluate(board[i+j*board_size]).as_long()]
            for i in range(board_size)]
            for j in range(board_size)]))


def input_tets():
    """ receives user input for the board size and tets

        Args: None

        Returns:
            board_size: the side length of the board (in cells)
            tets: a list of Tets represented as strings
    """
    tets = []
    print("Input the board size:")
    board_size = int(input())
    print("Input the number of tets for the game:")
    n_tets = int(input())
    print("Input the tets (Use 0 for no card and X for 10)")
    for _ in range(n_tets):
        tets.append(str(input()))
    return board_size, tets


if __name__ == "__main__":

    # get user input
    board_size, tets = input_tets()

    # setup board 
    board = board_v(board_size)

    # add clauses to solver
    s = Solver()
    s.add(board_c(board, board_size))
    s.add(tets_c(tets, board, board_size))
    s.add(distinct_index_c(tets))
    s.add(default_zero_c(tets, board))
    s.add(blackjack_c(board, board_size))

    # solve
    start = timeit.default_timer()
    if s.check() == sat:
        stop = timeit.default_timer()
        m = s.model()
        render_board(board)
        print(f"Runtime: {stop - start}s")
