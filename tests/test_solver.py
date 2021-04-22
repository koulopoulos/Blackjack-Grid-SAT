import sys
sys.path.append("../src")
import unittest
from z3 import *
from solver import *


"""
__    __   ______            _____   ______   __     __   ______  
|  \  |  \ /      \          |     \ /      \ |  \   |  \ /      \ 
| $$\ | $$|  $$$$$$\          \$$$$$|  $$$$$$\| $$   | $$|  $$$$$$\
| $$$\| $$| $$  | $$            | $$| $$__| $$| $$   | $$| $$__| $$
| $$$$\ $$| $$  | $$       __   | $$| $$    $$ \$$\ /  $$| $$    $$
| $$\$$ $$| $$  | $$      |  \  | $$| $$$$$$$$  \$$\  $$ | $$$$$$$$
| $$ \$$$$| $$__/ $$      | $$__| $$| $$  | $$   \$$ $$  | $$  | $$
| $$  \$$$ \$$    $$       \$$    $$| $$  | $$    \$$$   | $$  | $$
 \$$   \$$  \$$$$$$         \$$$$$$  \$$   \$$     \$     \$$   \$$ 
 """


class TestSolver(unittest.TestCase):

    def test_board_v(self):
        ex_vars_1 = [Int("b_0")]
        ex_vars_2 = [Int("b_0"), Int("b_1"), 
                     Int("b_2"), Int("b_3")]
        ex_vars_3 = [Int("b_0"), Int("b_1"), Int("b_2"), 
                     Int("b_3"), Int("b_4"), Int("b_5"),
                     Int("b_6"), Int("b_7"), Int("b_8")]
        self.assertEqual(board_v(1), ex_vars_1)
        self.assertEqual(board_v(2), ex_vars_2)
        self.assertEqual(board_v(3), ex_vars_2)

    def test_card_v(self):
        # Int(f"{rep}.{z}.idx__{i%2}_{i//2}")
        self.assertEqual(card_v("A", 0, 0), Int("A.0.idx__0_0"))
        self.assertEqual(card_v("2", 1, 0), Int("2.1.idx__0_0"))
        self.assertEqual(card_v("5", 0, 1), Int("5.1.idx__1_0"))

    def test_blackjack(self):
        bs = 2
        tetno = 3
        tets = [ "AAAA", "KKK0", "8888"]
        board = board_v(bs)
        print(blackjack_c(board, bs))
        


if __name__ == "__main__":
    unittest.main()
