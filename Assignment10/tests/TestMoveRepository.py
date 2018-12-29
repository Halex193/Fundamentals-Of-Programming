from unittest import TestCase

from model.Move import Move
from repository.MoveRepository import MoveRepository, DuplicateMoveError


class TestMoveRepository(TestCase):
    def setUp(self):
        self.moveRepository = MoveRepository()

    def testAddMove(self):
        move = Move("X", 0, 0)
        self.moveRepository.addMove(move)
        self.assertEqual(self.moveRepository.getMove(0, 0), move)
        self.assertEqual(self.moveRepository.getMove(1, 1), None)
        with self.assertRaises(DuplicateMoveError):
            self.moveRepository.addMove(move)

    def testMoves(self):
        move = Move("X", 0, 0)
        self.moveRepository.addMove(move)
        self.assertEqual(self.moveRepository.moves[0][0], move)
        self.assertEqual(self.moveRepository.moves[1][1], None)

    def testLastMove(self):
        move = Move("X", 0, 0)
        self.moveRepository.addMove(move)
        self.assertEqual(self.moveRepository.lastMove, move)

    def testMoveNumber(self):
        move = Move("X", 0, 0)
        self.moveRepository.addMove(move)
        self.assertEqual(self.moveRepository.moveNumber, 1)
