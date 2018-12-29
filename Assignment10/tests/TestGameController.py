from unittest import TestCase

from controllers.GameController import GameController
from model.Move import Move
from repository.MoveRepository import MoveRepository


class TestGameController(TestCase):
    def setUp(self):
        self.repo = MoveRepository()
        self.move = Move("X", 0, 0)
        self.repo.addMove(self.move)
        self.controller = GameController(self.repo)

    def testGetMoves(self):
        self.assertEqual(self.controller.getMoves()[0][0], self.move)

    def testResetGame(self):
        self.controller.resetGame()
        self.assertEqual(self.controller.getMoves()[0][0], None)

    def testGameStatus(self):
        self.assertEqual(self.controller.gameStatus(), 0)
        self.repo.addMove(Move("X", 1, 1))
        self.repo.addMove(Move("X", 2, 2))
        self.repo.addMove(Move("X", 3, 3))
        self.repo.addMove(Move("X", 4, 4))
        self.assertEqual(self.controller.gameStatus(), 1)
