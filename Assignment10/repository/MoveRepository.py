class DuplicateMoveError(RuntimeError):
    pass


class MoveRepository:
    """
    Represents a collection of moves on the board
    """
    dimX = 15
    dimY = 15
    winNumber = 5

    def __init__(self):
        self.__moves = []
        for i in range(MoveRepository.dimY):
            self.moves.append([])
            for j in range(MoveRepository.dimX):
                self.moves[i].append(None)
        self.__lastMove = None
        self.__moveNumber = 0

    def addMove(self, move):
        """
        Adds a move to the board
        :param move: The move to be added to the board
        :raises DuplicateMoveError: If the move has already been made on the board
        """
        if self.moves[move.y][move.x] is not None:
            raise DuplicateMoveError
        self.moves[move.y][move.x] = move
        self.__lastMove = move
        self.__moveNumber += 1

    def getMove(self, x, y):
        """
        Gets a specific move by its coordinates
        :param x: The x coordinate
        :param y: The y coordinate
        :return: The move that was made at the given coordinates
        """
        return self.moves[y][x]

    @property
    def moves(self):
        return self.__moves

    @property
    def lastMove(self):
        return self.__lastMove

    @property
    def moveNumber(self):
        return self.__moveNumber
