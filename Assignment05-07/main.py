"""
Main module
"""
from datetime import datetime

from logic.ControllerWrapper import ControllerWrapper
from repository.RepositoryWrapper import RepositoryWrapper
from ui.menuUI import *


def run():
    repositoryWrapper = RepositoryWrapper()
    now = datetime.now()
    currentDate = datetime.date(now.year, now.month, now.day)
    controllerWrapper = ControllerWrapper(repositoryWrapper)
    controllerWrapper.populateRepository()
    menuUI = MenuUI(controllerWrapper)
    menuUI.run()


if __name__ == '__main__':
    run()
