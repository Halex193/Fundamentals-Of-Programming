from controllers.AIPlayer import AIPlayer
from utils.Settings import Settings
from controllers.GameController import GameController
from controllers.Player import Player
from repository.MoveRepository import MoveRepository
from ui.UI import UI
from ui.ConsoleUI import ConsoleUI
from ui.GUI import GUI

settings = Settings()
moveRepository = MoveRepository()
gameController = GameController(moveRepository)

player1 = Player("X", moveRepository)
if settings["player1"] == "machine":
    player1 = AIPlayer(player1, gameController)

player2 = Player("O", moveRepository)
if settings["player2"] == "machine":
    player2 = AIPlayer(player2, gameController)

ui: UI = None
if settings["ui"] == "GUI":
    ui = GUI(player1, player2, gameController)
else:
    ui = ConsoleUI(player1, player2, gameController)
ui.run()
