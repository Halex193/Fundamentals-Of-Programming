class DuplicateMoveError(RuntimeError):
    pass


class MoveRepository:
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
        if self.moves[move.y][move.x] is not None:
            raise DuplicateMoveError
        self.moves[move.y][move.x] = move
        self.__lastMove = move
        self.__moveNumber += 1

    def getMove(self, x, y):
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
