import os

from prettytable import PrettyTable

from controllers.AIPlayer import AIPlayer
from controllers.Player import Player
from repository.MoveRepository import MoveRepository, DuplicateMoveError
from ui.UI import UI
from validation.Validator import MoveInvalid


class ConsoleUI(UI):
    def __init__(self, player1, player2, gameController):
        super().__init__(player1, player2, gameController)
        self.currentPlayer = player1

    def run(self):
        print("Welcome to Gomoku!")
        input("Press Enter key to start a new game\n")
        newGame = True
        while newGame:
            gameStatus = 0
            while gameStatus == 0:
                self.showBoard()
                if type(self.currentPlayer) is Player:
                    self.managePlayer()

                elif type(self.currentPlayer) is AIPlayer:
                    self.manageAI()

                gameStatus = self.gameController.gameStatus()

                if id(self.currentPlayer) == id(self.player1):
                    self.currentPlayer = self.player2
                else:
                    self.currentPlayer = self.player1

            if gameStatus == -1:
                print("The game has ended in a tie!")
            elif gameStatus == 1:
                if id(self.currentPlayer) == id(self.player1):
                    print("Player 2 has won!")
                else:
                    print("Player 1 has won!")
            choice = input("Would you like to start another game? yes/no\n")
            newGame = False
            if choice == "yes":
                newGame = True
                self.gameController.resetGame()
                self.currentPlayer = self.player1

    def manageAI(self):
        input("The AI player will make his move.\n Press Enter key to continue ")
        self.currentPlayer.makeMove()

    def managePlayer(self):
        inputValid = False
        while not inputValid:
            coordinates = input("Choose the coordinates for your move: ")
            coordinates = coordinates.strip()
            coordinates = coordinates.split(' ')
            if len(coordinates) != 2:
                print("Input invalid!")
            else:
                try:
                    xCoordinate = int(coordinates[0])
                    yCoordinate = int(coordinates[1])
                    self.currentPlayer.makeMove(xCoordinate, yCoordinate)
                    inputValid = True
                except ValueError:
                    print("Input invalid!")
                except MoveInvalid:
                    print("Invalid move!")
                except DuplicateMoveError:
                    print("Invalid move!")

    def showBoard(self):
        table = PrettyTable()
        fieldNames = [" "]
        for i in range(MoveRepository.dimensionX):
            fieldNames.append(str(i))
        table.field_names = fieldNames
        moves = self.gameController.getMoves()
        for i in range(MoveRepository.dimensionY):
            newRow = [str(i)]
            for move in moves[i]:
                newRow.append(move.sign if move is not None else " ")
            table.add_row(newRow)
            if i != MoveRepository.dimensionY - 1:
                table.add_row(["--"] * (MoveRepository.dimensionX + 1))
        table = table.get_string()
        os.system("cls")
        print(table)
