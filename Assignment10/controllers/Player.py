from model.Move import Move
from validation.Validator import Validator


class Player:
    """
    Provides the logic interface for a player
    """

    def __init__(self, sign, moveRepository):
        self.__sign = sign
        self.__moveRepository = moveRepository

    @property
    def sign(self):
        return self.__sign

    def makeMove(self, xCoordinate, yCoordinate):
        """
        Makes a move for the player
        :param xCoordinate: The x coordinate of the move
        :param yCoordinate: The y coordinate of the move
        """
        move = Move(self.sign, xCoordinate, yCoordinate)
        Validator.validateMove(move,
                               self.__moveRepository.lastMove.sign if self.__moveRepository.lastMove is not None else "")
        self.__moveRepository.addMove(move)

    def otherSign(self):
        """
        Returns the other sign
        """
        return "X" if self.sign == "O" else "O"
