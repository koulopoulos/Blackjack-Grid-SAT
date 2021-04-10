# represents a card-tet in a game of Blackjack Grid
class Tet:

    def __init__(self, cards, shapes, rand):
        self.grid = self.init(cards, shapes, rand)
    
    def init(self, cards, shapes, rand):
        """Produces a card tet by the given parameters 

        Args:
            cards: the set of cards from which the tet can be made
            shapes: the set of tet shapes to choose from
            rand: a random object

        Returns:
            grid: a 2D list representing a card tet
        """
        grid = [[0, 0], 
                [0, 0]]
        for posn in shapes[rand.randint(0, len(shapes) - 1)]:    
            grid[posn[1]][posn[0]] = rand.choice(list(cards.keys()))
        return grid

    def max_x(self):
        """Determines the maximum x-coordinate occupied in this tet's grid

        Returns: 
            the maximum x-coordinate
        """
        if self.grid[0][1] != 0 or self.grid[1][1] != 0:
            return 1
        else:
            return 0

    def max_y(self):
        """Determines the maximum y-coordinate occupied in this tet's grid

        Returns: 
            the maximum y-coordinate
        """
        if self.grid[1][0] != 0 or self.grid[1][1] != 0:
            return 1
        else:
            return 0
