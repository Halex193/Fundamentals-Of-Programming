from repository.MoveRepository import MoveRepository


class MoveInvalid(RuntimeError):
    pass


class Validator:

    @staticmethod
    def validateMove(move, sign, lastMoveSign):
        Validator.validateCoordinates(move.x, move.y)
        if lastMoveSign == sign:
            raise MoveInvalid

    @staticmethod
    def validateCoordinates(x, y):
        if not Validator.between(x, 0, MoveRepository.dimX - 1):
            raise MoveInvalid
        if not Validator.between(y, 0, MoveRepository.dimY - 1):
            raise MoveInvalid

    @staticmethod
    def between(a, b, c):
        return b <= a <= c
