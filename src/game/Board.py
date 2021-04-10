from .Tet import Tet

class Board:
    """To represent a board from a game of Blackjack Grid

    Fields:
        size: the side length of this board (square)
        grid: the 2D list representing this board's grid
    """

    def __init__(self, size):
        self.size = size
        self.grid = self.init_grid()
    
    def init_grid(self):
        """Creates a 2D list which represents an empty
           Blackjack Grid board (all cells set to 0)

        Returns:
            board: returns an empty board
        """
        board = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append(0)
            board.append(row)
        return board

    def is_inside(self, tet, x, y):
        """Can the given tet be placed at the given coordinates
           and remain completely inside of the board boundaries?

        Args:
            tet: the card Tet to test placement of
            x: a board x-coordinate
            y: a board y-coordinate

        Returns:
            boolean: is the tet within the board boundaries?
        """
        return (x + tet.max_x() <= self.size - 1 and y + tet.max_y() <= self.size - 1)

    def collides(self, tet, x, y):
        """Do the cards in the given tet collide with cards on the 
           board when the tet is placed at the given coordinates?

        Args:
            tet: the card Tet to test placement of
            x: a board x-coordinate
            y: a board y-coordinate

        Returns:
            boolean: is there a collision?
        """
        for dx in range(2):
            for dy in range(2):
                if self.grid[y+dy][x+dx] != 0 and tet.grid[dy][dx] != 0:
                    return True
        return False

    def is_valid(self, tet, x, y):
        """Can the given tet be placed at the given coordinates
           without causing a collision or being out of bounds?

        Args:
            tet: the card Tet to test placement of
            x: a board x-coordinate
            y: a board y-coordinate

        Returns:
            boolean: is the placement valid?
        """
        return self.is_inside(tet, x, y) and not self.collides(tet, x, y)
            
    