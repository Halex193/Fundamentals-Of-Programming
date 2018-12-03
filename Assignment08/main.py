"""
Main module
"""
from ui.GUI import GUI
from utils.Settings import Settings
from datetime import datetime, date

from repository.RepositoryWrapper import RepositoryWrapper
from logic.ControllerWrapper import ControllerWrapper
from ui.MenuUI import *


def run():
    settings = Settings()
    repositoryWrapper = RepositoryWrapper(
        settings["repository"],
        settings["studentsFile"],
        settings["gradesFile"],
        settings["assignmentsFile"]
    )
    now = datetime.now()
    currentDate = date(now.year, now.month, now.day)
    controllerWrapper = ControllerWrapper(repositoryWrapper, currentDate)
    if repositoryWrapper.isEmpty():
        controllerWrapper.populateRepository()

    ui: UI = None
    if settings["ui"] == "GUI":
        ui = GUI(controllerWrapper)
    else:
        ui = MenuUI(controllerWrapper)
    ui.run()


if __name__ == '__main__':
    run()
