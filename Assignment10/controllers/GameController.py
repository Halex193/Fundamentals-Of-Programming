from repository.MoveRepository import MoveRepository
from validation.Validator import Validator, MoveInvalid


class GameController:
    def __init__(self, moveRepository):
        self.__moveRepository = moveRepository

    def getMoves(self):
        return self.__moveRepository.moves

    def resetGame(self):
        self.__moveRepository.__init__()

    def gameStatus(self):
        lastMove = self.__moveRepository.lastMove

        directions = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1)
        ]

        for direction in directions:
            if self.count(lastMove, direction) + self.count(lastMove,
                                                            self.invert(direction)) + 1 == MoveRepository.winNumber:
                return 1
        if self.__moveRepository.moveNumber == MoveRepository.dimX * MoveRepository.dimY:
            return -1
        return 0

    def count(self, lastMove, direction):
        count = 0
        x = lastMove.x
        y = lastMove.y
        x += direction[0]
        y += direction[1]
        while self.isValid(x, y) and self.__moveRepository.getMove(x, y) is not None\
                and self.__moveRepository.getMove(x, y).sign == lastMove.sign:
            x += direction[0]
            y += direction[1]
            count += 1
        return count

    @staticmethod
    def invert(direction):
        return -direction[0], -direction[1]

    @staticmethod
    def isValid(x, y):
        try:
            Validator.validateCoordinates(x, y)
            return True
        except MoveInvalid:
            return False
