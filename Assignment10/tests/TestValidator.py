from unittest import TestCase

from model.Move import Move
from validation.Validator import Validator, MoveInvalid


class TestValidator(TestCase):
    def setUp(self):
        self.move1 = Move("X", 0, 0)
        self.move2 = Move("O", -1, 0)

    def test_validateMove(self):
        Validator.validateMove(self.move1, "O")
        with self.assertRaises(MoveInvalid):
            Validator.validateMove(self.move2, "X")

    def test_validateCoordinates(self):
        Validator.validateCoordinates(5, 5)
        with self.assertRaises(MoveInvalid):
            Validator.validateCoordinates(-1, 20)
        with self.assertRaises(MoveInvalid):
            Validator.validateCoordinates(-1, 12)
        with self.assertRaises(MoveInvalid):
            Validator.validateCoordinates(0, 20)
