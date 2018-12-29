from repository.MoveRepository import MoveRepository
from validation.Validator import Validator, MoveInvalid


class GameController:
    """
    Provides the main game logic
    """
    def __init__(self, moveRepository):
        self.__moveRepository = moveRepository

    def getMoves(self):
        """
        Returns the move matrix
        :return: A list of lists of moves
        """
        return self.__moveRepository.moves

    def resetGame(self):
        """
        Resets the game
        """
        self.__moveRepository.__init__()

    def gameStatus(self):
        """
        Provides information about the game status
        :returns: 1 if the game has been won by the last player who moved
                -1 if the game ended in a tie
                 0 if the game can be continued
        """
        lastMove = self.__moveRepository.lastMove

        directions = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1)
        ]

        for direction in directions:
            if self.__count(lastMove, direction) + self.__count(lastMove,
                                                                self.__invert(direction)) + 1 == MoveRepository.winNumber:
                return 1
        if self.__moveRepository.moveNumber == MoveRepository.dimX * MoveRepository.dimY:
            return -1
        return 0

    def __count(self, lastMove, direction):
        """
        Counts the signs similar to the last move's in the given direction and returns the result
        :param lastMove: The last move made in the game
        :param direction: The direction to use in the calculation
        :return: The number of similar signs in the given direction
        """
        count = 0
        x = lastMove.x
        y = lastMove.y
        x += direction[0]
        y += direction[1]
        while self.__isValid(x, y) and self.__moveRepository.getMove(x, y) is not None\
                and self.__moveRepository.getMove(x, y).sign == lastMove.sign:
            x += direction[0]
            y += direction[1]
            count += 1
        return count

    @staticmethod
    def __invert(direction):
        """
        Inverts a direction
        """
        return -direction[0], -direction[1]

    @staticmethod
    def __isValid(x, y):
        """
        Checks if the given coordinates are valid
        """
        try:
            Validator.validateCoordinates(x, y)
            return True
        except MoveInvalid:
            return False
