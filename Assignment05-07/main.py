"""
Main module
"""
from datetime import datetime

from menuUI import *


def run():
    repository = Repository()
    now = datetime.now()
    currentDate = date(now.year, now.month, now.day)
    logicComponent = LogicComponent(repository, currentDate)
    logicComponent.populateRepository()
    menuUI = MenuUI(logicComponent)
    menuUI.run()


if __name__ == '__main__':
    run()
