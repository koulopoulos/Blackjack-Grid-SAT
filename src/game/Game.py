import numpy as np
from .Board import Board
from .Tet import Tet

class Game:
    """To represent a game of Blackjack Grid

    Fields:
        rand: random number generator
        cards: the set of cards with which this game is played
        shapes: the set of tet shapes that are used in this game
        board: a Board object to represent 
        tets: a list of Tet objects to represent all tets in this game
    """

    def __init__(self, size, n_tets, rand):
        self.rand = rand
        self.cards = {
            "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, 
            "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, 
            "J": 10, "Q": 10, "K": 10
        }
        self.shapes = [
            # 1-tet
            {(0, 0)}, {(1, 0)}, {(0, 1)}, {(1, 1)},
            # I-tet
            {(0, 0), (1, 0)}, {(0, 0), (0, 1)},
            {(1, 0), (1, 1)}, {(0, 1), (1, 1)},
            # L-tet
            {(0, 0), (1, 0), (1, 1)},
            {(0, 0), (0, 1), (1, 1)},
            {(0, 0), (1, 0), (0, 1)},
            {(1, 0), (1, 1), (0, 1)},
            # O-tet
            {(0, 0), (1, 0), (0, 1), (1, 1)}]
        self.board = Board(size)
        self.tets = self.generate_tets(n_tets)

    def generate_tets(self, n_tets):
        tets = []
        for n in range(n_tets):
            tets.append(Tet(self.cards, self.shapes, self.rand))
        return tets

    def tets_repr(self):
        return str(np.array([tet.grid for tet in self.tets]))

    def board_repr(self):
        return str(np.array(self.board.grid))