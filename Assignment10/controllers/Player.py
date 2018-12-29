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

    def makeMove(self, x, y):
        """
        Makes a move for the player
        :param x: The x coordinate of the move
        :param y: The y coordinate of the move
        """
        move = Move(self.sign, x, y)
        Validator.validateMove(move,
                               self.__moveRepository.lastMove.sign if self.__moveRepository.lastMove is not None else "")
        self.__moveRepository.addMove(move)
