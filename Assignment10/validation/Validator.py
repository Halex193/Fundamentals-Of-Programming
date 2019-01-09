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
        Validator.validateCoordinates(move.xCoordinate, move.yCoordinate)
        if lastMoveSign == move.sign:
            raise MoveInvalid

    @staticmethod
    def validateCoordinates(xCoordinate, yCoordinate):
        """
        Validates the coordinates of a move
        :param xCoordinate: The x coordinate
        :param yCoordinate: The y coordinate
        :raises MoveInvalid: If the move is invalid
        """
        if not 0 <= xCoordinate < MoveRepository.dimensionX:
            raise MoveInvalid
        if not 0 <= yCoordinate < MoveRepository.dimensionY:
            raise MoveInvalid
