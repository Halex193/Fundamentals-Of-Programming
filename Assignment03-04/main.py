import consoleUI
import menuUI
from test import run_tests


def run():
    print("Welcome to the apartment management software!")
    print("Choose the form of User Interface you want to use:")
    print("1. Console based UI")
    print("2. Menu based UI")
    choice = input("Your choice: ")
    try:
        choice = int(choice)
    except ValueError:
        return

    if choice == 1:
        consoleUI.run()
    elif choice == 2:
        menuUI.run()


run_tests()
run()
