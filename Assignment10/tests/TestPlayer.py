from unittest import TestCase

from controllers.Player import Player
from repository.MoveRepository import MoveRepository


class TestPlayer(TestCase):
    def testMakeMove(self):
        repository = MoveRepository()
        player = Player("X", repository)
        player.makeMove(0, 0)
        self.assertEqual(repository.getMove(0, 0).sign, "X")
