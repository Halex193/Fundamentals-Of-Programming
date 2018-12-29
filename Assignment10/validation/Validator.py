from repository.MoveRepository import MoveRepository


class MoveInvalid(RuntimeError):
    pass


class Validator:
    """
    Validates program data
    """

    @staticmethod
    def validateMove(move, lastMoveSign):
        """
        Validates a move
        :param move: The move to be validated
        :param lastMoveSign: The sign of the last move
        :raises MoveInvalid: If the move is invalid
        """
        Validator.validateCoordinates(move.x, move.y)
        if lastMoveSign == move.sign:
            raise MoveInvalid

    @staticmethod
    def validateCoordinates(x, y):
        """
        Validates the coordinates of a move
        :param x: The x coordinate
        :param y: The y coordinate
        :raises MoveInvalid: If the move is invalid
        """
        if not 0 <= x < MoveRepository.dimX:
            raise MoveInvalid
        if not 0 <= y < MoveRepository.dimY:
            raise MoveInvalid
