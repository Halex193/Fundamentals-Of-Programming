class Move:
    """
    Represents a move made on the game board
    """
    def __init__(self, sign, x, y):
        self.y = y
        self.x = x
        self.sign = sign
