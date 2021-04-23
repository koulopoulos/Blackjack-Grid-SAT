import sys
sys.path.append("../")
import unittest
from z3 import *
from src.solver import *


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
        self.assertEqual(board_v(3), ex_vars_3)

    def test_card_v(self):
        self.assertEqual(card_v("A", 0, 0), Int("A.0.idx__0_0"))
        self.assertEqual(card_v("2", 1, 0), Int("2.1.idx__0_0"))
        self.assertEqual(card_v("5", 0, 1), Int("5.0.idx__1_0"))
        self.assertEqual(card_v("6", 2, 2), Int("6.2.idx__0_1"))
        self.assertEqual(card_v("6", 3, 4), Int("6.3.idx__0_2"))
        self.assertEqual(card_v("X", 8, 5), Int("X.8.idx__1_2"))

    def test_board_c(self):
        ex_c_1 = [And(Int("b_0") >= 0, Int("b_0") <= 13)]
        ex_c_2 = [And(Int("b_0") >= 0, Int("b_0") <= 13),
                  And(Int("b_1") >= 0, Int("b_1") <= 13),
                  And(Int("b_2") >= 0, Int("b_2") <= 13),
                  And(Int("b_3") >= 0, Int("b_3") <= 13)]
        self.assertEqual(board_c(board_v(1), 1), ex_c_1)
        self.assertEqual(board_c(board_v(2), 2), ex_c_2)

    def test_tets_c(self):
        ex_c_1 = And(And(And(Int("A.0.idx__0_0") >= 0, Int("A.0.idx__0_0") <= 0),
                     And(Implies(Int("A.0.idx__0_0") == 0, Int("b_0") == 1)),
                     And(Int("A.0.idx__1_0") >= 0, Int("A.0.idx__1_0") <= 0),
                     And(Implies(Int("A.0.idx__1_0") == 0, Int("b_0") == 1)),
                     And(Int("A.0.idx__0_1") >= 0, Int("A.0.idx__0_1") <= 0),
                     And(Implies(Int("A.0.idx__0_1") == 0, Int("b_0") == 1)),
                     And(Int("A.0.idx__1_1") >= 0, Int("A.0.idx__1_1") <= 0),
                     And(Implies(Int("A.0.idx__1_1") == 0, Int("b_0") == 1)),
                     And(Not(Or(Int("A.0.idx__1_0")%1 == 0, Int("A.0.idx__1_0")%1 == 0)),
                     Int("A.0.idx__0_0") == Int("A.0.idx__1_0") - 1,
                     Int("A.0.idx__0_0") == Int("A.0.idx__0_1") - 1,
                     Int("A.0.idx__0_0") == Int("A.0.idx__1_1") - 1 - 1)))
        ex_c_2 = And(And(And(Int("4.0.idx__0_0") >= 0, Int("4.0.idx__0_0") <= 0),
                     And(Implies(Int("4.0.idx__0_0") == 0, Int("b_0") == 4)),
                     And(Int("4.0.idx__1_0") >= 0, Int("4.0.idx__1_0") <= 0),
                     And(Implies(Int("4.0.idx__1_0") == 0, Int("b_0") == 4)),
                     And(Int("4.0.idx__0_1") >= 0, Int("4.0.idx__0_1") <= 0),
                     And(Implies(Int("4.0.idx__0_1") == 0, Int("b_0") == 4)),
                     And(Int("4.0.idx__1_1") >= 0, Int("4.0.idx__1_1") <= 0),
                     And(Implies(Int("4.0.idx__1_1") == 0, Int("b_0") == 4)),
                     And(Not(Or(Int("4.0.idx__1_0")%1 == 0, Int("4.0.idx__1_0")%1 == 0)),
                     Int("4.0.idx__0_0") == Int("4.0.idx__1_0") - 1,
                     Int("4.0.idx__0_0") == Int("4.0.idx__0_1") - 1,
                     Int("4.0.idx__0_0") == Int("4.0.idx__1_1") - 1 - 1)))
        self.assertEqual(tets_c(["AAAA"], board_v(1), 1), ex_c_1)
        self.assertEqual(tets_c(["4444"], board_v(1), 1), ex_c_2)

    def test_distinct_index_c(self):
        ex_c_1 = Distinct(Int("2.0.idx__0_0"), Int("3.0.idx__1_0"), 
                          Int("4.0.idx__0_1"), Int("5.0.idx__1_1"))
        ex_c_2 = Distinct(Int("K.0.idx__0_0"), Int("K.0.idx__1_0"), 
                          Int("K.0.idx__0_1"), Int("K.0.idx__1_1"))
        ex_c_3 = Distinct(Int("J.0.idx__0_0"), Int("J.0.idx__1_0"),
                          Int("J.0.idx__0_1"), Int("J.0.idx__1_1"),
                          Int("Q.1.idx__0_0"), Int("Q.1.idx__1_0"), 
                          Int("Q.1.idx__0_1"), Int("Q.1.idx__1_1"))
        self.assertEqual(distinct_index_c(["2345"]), ex_c_1)
        self.assertEqual(distinct_index_c(["KKKK"]), ex_c_2)
        self.assertEqual(distinct_index_c(["JJJJ", "QQQQ"]), ex_c_3)

    def test_range_c(self):
        # range_c(rep, z, i, board_size)
        ex_c_1 = And(Int("X.0.idx__0_0") >= 0, Int("X.0.idx__0_0") <= 0)
        print(range_c("9", 2, 1, 0))
        ex_c_2 = And(Int("9.2.idx__1_0") >= 0, Int("9.2.idx__1_0") <= -1)
        self.assertEqual(range_c("X", 0, 0, 1), ex_c_1)
        self.assertEqual(range_c("9", 2, 1, 0), ex_c_2)

    def test_blackjack(self):
        bs = 1
        board = board_v(bs)
        self.assertEqual(
            blackjack_c(board, bs),
            Or(Or(0 + If(Int("b_0") > 10, 10, Int("b_0")) == 21,
                  0 + If(Int("b_0") > 10, 10, Int("b_0")) == 21)))

    def test_relative_c(self):
        self.assertEqual(relative_c(1,'A000', 1), 
            And(Int("A.1.idx__0_0") == Int("0.1.idx__1_0") - 1,
            Int("A.1.idx__0_0") == Int("0.1.idx__0_1") - 1,
            Int("A.1.idx__0_0") == Int("0.1.idx__1_1") - 1 - 1))
    
    def test_default_zero_c(self):
        board = board_v(2)
        board2 = board_v(1)
        tets = ['AAAA', 'KKKK']
        tets2 = ['A000']
        self.assertEqual(default_zero_c(tets, board, 2),
                        And(Implies(Not(Or(Int("A.0.idx__0_0") == 0,
                                        Int("A.0.idx__1_0") == 0,
                                        Int("A.0.idx__0_1") == 0,
                                        Int("A.0.idx__1_1") == 0,
                                        Int("K.1.idx__0_0") == 0,
                                        Int("K.1.idx__1_0") == 0,
                                        Int("K.1.idx__0_1") == 0,
                                        Int("K.1.idx__1_1") == 0)),
                                        Int("b_0") == 0),
                            Implies(Not(Or(Int("A.0.idx__0_0") == 1,
                                           Int("A.0.idx__1_0") == 1,
                                           Int("A.0.idx__0_1") == 1,
                                           Int("A.0.idx__1_1") == 1,
                                           Int("K.1.idx__0_0") == 1,
                                           Int("K.1.idx__1_0") == 1,
                                           Int("K.1.idx__0_1") == 1,
                                           Int("K.1.idx__1_1") == 1)),
                                        Int("b_1") == 0),
                            Implies(Not(Or(Int("A.0.idx__0_0") == 2,
                                        Int("A.0.idx__1_0") == 2,
                                        Int("A.0.idx__0_1") == 2,
                                        Int("A.0.idx__1_1") == 2,
                                        Int("K.1.idx__0_0") == 2,
                                        Int("K.1.idx__1_0") == 2,
                                        Int("K.1.idx__0_1") == 2,
                                        Int("K.1.idx__1_1") == 2)),
                                        Int("b_2") == 0),
                            Implies(Not(Or(Int("A.0.idx__0_0") == 3,
                                           Int("A.0.idx__1_0") == 3,
                                           Int("A.0.idx__0_1") == 3,
                                           Int("A.0.idx__1_1") == 3,
                                           Int("K.1.idx__0_0") == 3,
                                           Int("K.1.idx__1_0") == 3,
                                           Int("K.1.idx__0_1") == 3,
                                           Int("K.1.idx__1_1") == 3)),
                                        Int("b_3") == 0)))

    def test_assignment_c(self):
        board = board_v(1)
        self.assertEqual(assignment_c("A", 1, 2, board, 1),
                         And(Implies(Int("A.1.idx__0_1") == 0, Int("b_0") == 1)))
        self.assertEqual(assignment_c("9", 2, 2, board, 1),
                         And(Implies(Int("9.2.idx__0_1") == 0, Int("b_0") == 9)))

if __name__ == "__main__":
    unittest.main()
