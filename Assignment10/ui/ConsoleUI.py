from ui.UI import UI


class ConsoleUI(UI):
    def __init__(self, player1, player2, gameController):
        super().__init__(player1, player2, gameController)
        self.commands = {
            'show': self.show
        }

    def run(self):
        print("Hello!")

        while True:
            line = input("> ").strip()
            line = line.split(' ')
            command = line[0]
            arguments = line[1:]
            if command == 'exit':
                break
            if command in self.commands:
                self.commands[command](arguments)
            else:
                print("Command invalid!")

    def show(self, arguments):
        print("Mere!")
