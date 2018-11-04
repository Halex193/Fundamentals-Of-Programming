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
            InvalidStudentGroup: "Student group is invalid",
            InvalidAssignmentId: "Assignment id is invalid",
            InvalidAssignmentDeadline: "Assignment deadline is invalid",
            DuplicateAssignment: "Assignment was already given to student"
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
        AssignMenu(self.logicComponent).showMenu()


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
        studentId = input("Student id: ")
        try:
            student = self.logicComponent.findStudent(studentId)
            print("You are modifying the student with name " + student.getName() + " from group " + str(
                student.getGroup()))
            name = input("Student's new name: ")
            group = input("Student's new group: ")
            self.logicComponent.updateStudent(studentId, name, group)
            print("Student information updated")
        except CustomError as error:
            MenuUI.handleCustomError(error)


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
        assignmentList = self.logicComponent.listAssignments()
        print("\nID - Description - Deadline")
        for assignment in assignmentList:
            print(self.assignmentToStr(assignment))

    def addAssignment(self):
        description = input("Assignment's description: ")
        deadline = input("Assignment's deadline (format: day.month.year): ")
        try:
            self.logicComponent.addAssignment(description, deadline)
            print("Assignment added")
        except CustomError as error:
            MenuUI.handleCustomError(error)

    def removeAssignment(self):
        assignmentId = input("Assignment id: ")
        try:
            self.logicComponent.removeAssignment(assignmentId)
            print("Assignment removed")
        except CustomError as error:
            MenuUI.handleCustomError(error)

    def updateAssignment(self):
        assignmentId = input("Assignment id: ")
        try:
            assignment = self.logicComponent.findAssignment(assignmentId)
            print(
                "You are modifying the assignment with description '" + assignment.getDescription() +
                "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
            description = input("Assignment's new description: ")
            deadline = input("Assignment's new deadline (format: day.month.year): ")
            self.logicComponent.updateAssignment(assignmentId, description, deadline)
            print("Assignment information updated")
        except CustomError as error:
            MenuUI.handleCustomError(error)

    @staticmethod
    def assignmentToStr(assignment: Assignment):
        deadline = ManageAssignmentsMenu.dateToStr(assignment.getDeadline())
        return str(
            assignment.getAssignmentId()) + " - " + assignment.getDescription() + " - " + deadline

    @staticmethod
    def dateToStr(parameterDate: date):
        return str(parameterDate.day) + "." + str(parameterDate.month) + "." + str(parameterDate.year)


class AssignMenu(Menu):
    menuName = "Give assignments"

    def __init__(self, logicComponent: LogicComponent):
        super().__init__(logicComponent)

        self.optionList = [
            "1. Give assignment to student",
            "2. Give assignment to group of students",
            Menu.exitKey + ". Exit"
        ]
        self.choiceList = {
            '1': self.assignToStudent,
            '2': self.assignToGroup
        }

    def assignToStudent(self):
        try:
            studentId = input("Choose student id: ")
            student = self.logicComponent.findStudent(studentId)
            print("You giving an assignment to the student with name " + student.getName() + " from group " + str(
                student.getGroup()))
            assignmentId = input("Choose assignment id: ")
            assignment = self.logicComponent.findAssignment(assignmentId)
            print(
                "You are giving the assignment with description '" + assignment.getDescription() +
                "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
            self.logicComponent.assignToStudent(studentId, assignmentId)
            print("Assignment was given")
        except CustomError as error:
            MenuUI.handleCustomError(error)

    def assignToGroup(self):
        try:
            group = input("Choose group: ")
            self.logicComponent.checkGroupExistence(group)
            assignmentId = input("Choose assignment id: ")
            assignment = self.logicComponent.findAssignment(assignmentId)
            print(
                "You are giving the assignment with description '" + assignment.getDescription() +
                "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
            self.logicComponent.assignToGroup(group, assignmentId)
            print("Assignments were given")
        except CustomError as error:
            MenuUI.handleCustomError(error)
