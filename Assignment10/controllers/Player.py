from model.Move import Move
from validation.Validator import Validator


class Player:

    def __init__(self, sign, moveRepository):
        self.__sign = sign
        self.__moveRepository = moveRepository

    @property
    def sign(self):
        return self.__sign

    def makeMove(self, x, y):
        move = Move(self.sign, x, y)
        Validator.validateMove(move, self.__sign,
                               self.__moveRepository.lastMove.sign if self.__moveRepository.lastMove is not None else "")
        self.__moveRepository.addMove(move)
