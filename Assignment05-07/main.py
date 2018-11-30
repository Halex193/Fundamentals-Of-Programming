"""
Main module
"""
from datetime import datetime, date

from repository.RepositoryWrapper import RepositoryWrapper
from logic.ControllerWrapper import ControllerWrapper
from ui.menuUI import *


def run():
    repositoryWrapper = RepositoryWrapper('inmemory')
    now = datetime.now()
    currentDate = date(now.year, now.month, now.day)
    controllerWrapper = ControllerWrapper(repositoryWrapper, currentDate)
    controllerWrapper.populateRepository()
    menuUI = MenuUI(controllerWrapper)
    menuUI.run()


if __name__ == '__main__':
    run()
