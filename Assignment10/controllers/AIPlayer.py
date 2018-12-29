import random

from repository.MoveRepository import MoveRepository


class AIPlayer:
    def __init__(self, player, gameController):
        self.player = player
        self.gameController = gameController

    def makeMove(self):
        # TODO change logic
        moveValid = False
        while not moveValid:
            x = random.randint(0, MoveRepository.dimX - 1)
            y = random.randint(0, MoveRepository.dimY - 1)
            try:
                self.player.makeMove(x, y)
                moveValid = True
            except:
                pass
