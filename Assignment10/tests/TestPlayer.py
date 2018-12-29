from unittest import TestCase

from controllers.Player import Player
from repository.MoveRepository import MoveRepository


class TestPlayer(TestCase):
    def testMakeMove(self):
        repo = MoveRepository()
        player = Player("X", repo)
        player.makeMove(0, 0)
        self.assertEqual(repo.getMove(0, 0).sign, "X")
