class DuplicateMoveError(RuntimeError):
    pass


class MoveRepository:
    """
    Represents a collection of moves on the board
    """
    dimensionX = 15
    dimensionY = 15
    winNumber = 5

    def __init__(self):
        self.__moves = []
        for i in range(MoveRepository.dimensionY):
            self.moves.append([])
            for j in range(MoveRepository.dimensionX):
                self.moves[i].append(None)
        self.__lastMove = None
        self.__moveNumber = 0

    def addMove(self, move):
        """
        Adds a move to the board
        :param move: The move to be added to the board
        :raises DuplicateMoveError: If the move has already been made on the board
        """
        if self.moves[move.yCoordinate][move.xCoordinate] is not None:
            raise DuplicateMoveError
        self.moves[move.yCoordinate][move.xCoordinate] = move
        self.__lastMove = move
        self.__moveNumber += 1

    def getMove(self, xCoordinate, yCoordinate):
        """
        Gets a specific move by its coordinates
        :param xCoordinate: The x coordinate
        :param yCoordinate: The y coordinate
        :return: The move that was made at the given coordinates
        """
        return self.moves[yCoordinate][xCoordinate]

    def undoMove(self, xCoordinate, yCoordinate, lastMove):
        if self.moves[yCoordinate][xCoordinate] is None:
            raise DuplicateMoveError
        self.moves[yCoordinate][xCoordinate] = None
        self.__moveNumber -= 1
        self.__lastMove = lastMove

    @property
    def moves(self):
        return self.__moves

    @property
    def lastMove(self):
        return self.__lastMove

    @property
    def moveNumber(self):
        return self.__moveNumber
