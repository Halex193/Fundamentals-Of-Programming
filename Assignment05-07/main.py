"""
Main module
"""
from logic import LogicComponent
from repository import Repository
from menuUI import *


def run():
    repository = Repository()
    logicComponent = LogicComponent(repository)
    menuUI = MenuUI(logicComponent)
    menuUI.run()


if __name__ == '__main__':
    run()
