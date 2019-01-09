class Move:
    """
    Represents a move made on the game board
    """
    def __init__(self, sign, xCoordinate, yCoordinate):
        self.yCoordinate = yCoordinate
        self.xCoordinate = xCoordinate
        self.sign = sign
