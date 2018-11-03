"""
This is the menu UI module
"""

from logic import *
from typing import *


class MenuUI:

    def __init__(self, logicComponent: LogicComponent):
        self.logicComponent = logicComponent

    def run(self):
        MainMenu(self.logicComponent).showMenu()

    @classmethod
    def handleCustomError(cls, error):
        errorTypes = {
            CustomError: "Invalid data",
            InvalidStudentId: "Student id is invalid",
            InvalidStudentGroup: "Student group is invalid"
        }
        if type(error) in errorTypes:
            print(errorTypes[type(error)])
        else:
            raise error


class Menu:
    exitKey = 'x'
    menuName = 'Abstract menu'

    def __init__(self, logicComponent: LogicComponent):
        self.optionList = []
        self.choiceList = {}
        self.logicComponent = logicComponent

    def showMenu(self):
        while True:
            print()
            print("-- " + self.menuName + " --\n")
            print("Valid options: ")
            for option in self.optionList:
                print(option)

            valid = False
            while not valid:
                choice = input("Your choice: ")
                if choice == Menu.exitKey:
                    return
                if choice in self.choiceList:
                    self.choiceList[choice]()
                    valid = True
                else:
                    print("Choice invalid")


class MainMenu(Menu):
    menuName = "Main menu"

    def __init__(self, logicComponent: LogicComponent):
        super().__init__(logicComponent)

        self.optionList = [
            "1. Manage students",
            "2. Manage assignments",
            "3. Give assignments",
            Menu.exitKey + ". Exit"
        ]
        self.choiceList = {
            '1': self.manageStudents,
            '2': self.manageAssignments,
            '3': self.giveAssignments
        }

    def manageStudents(self):
        ManageStudentsMenu(self.logicComponent).showMenu()

    def manageAssignments(self):
        ManageAssignmentsMenu(self.logicComponent).showMenu()

    def giveAssignments(self):
        pass


class ManageStudentsMenu(Menu):
    menuName = "Manage students"

    def __init__(self, logicComponent: LogicComponent):
        super().__init__(logicComponent)

        self.optionList = [
            "1. List students",
            "2. Add student",
            "3. Remove student",
            "4. Update student",
            Menu.exitKey + ". Back"
        ]
        self.choiceList = {
            '1': self.listStudents,
            '2': self.addStudent,
            '3': self.removeStudent,
            '4': self.updateStudent
        }

    def listStudents(self):
        studentList = self.logicComponent.listStudents()
        print("\nID - Name - Group")
        for student in studentList:
            print(self.studentToStr(student))

    @staticmethod
    def studentToStr(student: Student):
        return str(student.getStudentId()) + " - " + student.getName() + " - " + str(student.getGroup())

    def addStudent(self):
        name = input("Student's name: ")
        group = input("Student's group: ")
        try:
            self.logicComponent.addStudent(name, group)
            print("Student added")
        except CustomError as error:
            MenuUI.handleCustomError(error)

    def removeStudent(self):
        studentId = input("Student id: ")
        try:
            self.logicComponent.removeStudent(studentId)
            print("Student removed")
        except CustomError as error:
            MenuUI.handleCustomError(error)

    def updateStudent(self):
        pass
    # TODO here we go


class ManageAssignmentsMenu(Menu):
    menuName = "Manage assignments"

    def __init__(self, logicComponent: LogicComponent):
        super().__init__(logicComponent)

        self.optionList = [
            "1. List assignments",
            "2. Add assignment",
            "3. Remove assignment",
            "4. Update assignment",
            Menu.exitKey + ". Back"
        ]
        self.choiceList = {
            '1': self.listAssignments,
            '2': self.addAssignment,
            '3': self.removeAssignment,
            '4': self.updateAssignment
        }

    def listAssignments(self):
        pass

    def addAssignment(self):
        pass

    def removeAssignment(self):
        pass

    def updateAssignment(self):
        pass

    def giveAssignments(self):
        pass
