from game.BJG import BJG
import random as rand

if __name__ == "__main__":
    g = Game(6, 4, rand.Random())
    print(g.board_repr())
