import random

from model.Move import Move
from repository.MoveRepository import MoveRepository


class AIPlayer:
    def __init__(self, player, gameController):
        self.player = player
        self.gameController = gameController

    def makeMove(self):
        """
        Makes a move for the AI player
        """
        possibleMoves = []
        moves = self.gameController.getMoves()
        for i in range(MoveRepository.dimensionY):
            for j in range(MoveRepository.dimensionX):
                if moves[i][j] is None:
                    possibleMoves.append((j, i))

        move = self.searchBestMove(possibleMoves)
        if move is not None:
            self.player.makeMove(move[0], move[1])
            return
        move = self.moveNear(self.gameController.getLastMove(), possibleMoves)
        if move is not None:
            self.player.makeMove(move[0], move[1])
            return
        move = self.randomMove(possibleMoves)
        self.player.makeMove(move[0], move[1])

    def searchBestMove(self, possibleMoves):
        """
        Searches for a move that wins or blocks the winning of the opponent
        :param possibleMoves: The moves that are possible
        :return: The winning/blocking move, or None if it does not exists
        """
        for move in possibleMoves:
            lastMove = self.gameController.getLastMove()
            self.player.makeMove(move[0], move[1])
            gameStatus = self.gameController.gameStatus()
            self.gameController.moveRepository.undoMove(move[0], move[1], lastMove)
            if gameStatus == 1:
                return move

        for move in possibleMoves:
            lastMove = self.gameController.getLastMove()
            self.gameController.moveRepository.addMove(Move(self.player.otherSign(), move[0], move[1]))
            gameStatus = self.gameController.gameStatus()
            self.gameController.moveRepository.undoMove(move[0], move[1], lastMove)
            if gameStatus == 1:
                return move

    def moveNear(self, lastMove, possibleMoves):
        """
        Returns a move near the last one, if it exists
        :param lastMove: The last move made
        :param possibleMoves: The possible moves
        :return: The move near the last one or None if it does not exist
        """
        if lastMove is None:
            return
        random.shuffle(possibleMoves)
        for move in possibleMoves:
            if abs(lastMove.xCoordinate - move[0]) <= 1 and abs(lastMove.yCoordinate - move[1]) <= 1:
                return move

    def randomMove(self, possibleMoves):
        """
        Picks a random move from the possible ones
        """
        return possibleMoves[random.randint(0, len(possibleMoves) - 1)]
