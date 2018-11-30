"""
This is the menu UI module
"""
import os
from datetime import date

from logic import *
from logic.AssignmentController import AssignmentController
from logic.ControllerWrapper import ControllerWrapper
from logic.StudentController import StudentController
from model.Assignment import Assignment
from model.Student import Student


class MenuUI:

    def __init__(self, controllerWrapper: ControllerWrapper):
        self.controllerWrapper = controllerWrapper

    def run(self):
        MainMenu(self.controllerWrapper).showMenu()

    @classmethod
    def handleCustomError(cls, error):
        errorTypes = {
            CustomError: "Invalid data",
            InvalidStudentId: "Student id is invalid",
            InvalidStudentGroup: "Student group is invalid",
            InvalidAssignmentId: "Assignment id is invalid",
            InvalidAssignmentDeadline: "Assignment deadline is invalid",
            DuplicateAssignment: "Assignment was already given to student",
            InvalidGrade: "Grade must be an integer between 0 and 10"
        }
        if type(error) in errorTypes:
            print(errorTypes[type(error)])
        else:
            raise error


class Menu:
    exitKey = 'x'
    menuName = 'Abstract menu'

    def __init__(self, controllerWrapper: ControllerWrapper):
        self.optionList = []
        self.choiceList = {}
        self.controllerWrapper = controllerWrapper

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
                    self.clearScreen()
                    return
                if choice in self.choiceList:
                    try:
                        self.clearScreen()
                        self.choiceList[choice]()
                    except CustomError as error:
                        MenuUI.handleCustomError(error)
                    valid = True
                else:
                    print("Choice invalid")

    @staticmethod
    def clearScreen():
        os.system('cls')


class MainMenu(Menu):
    menuName = "Main menu"

    def __init__(self, controllerWrapper: ControllerWrapper):
        super().__init__(controllerWrapper)

        self.optionList = [
            "1. Manage students",
            "2. Manage assignments",
            "3. Give assignments",
            "4. Grade student",
            "5. Show statistics",
            "6. Undo",
            "7. Redo",
            "8. List repository",
            Menu.exitKey + ". Exit"
        ]
        self.choiceList = {
            '1': self.manageStudents,
            '2': self.manageAssignments,
            '3': self.giveAssignments,
            '4': self.gradeStudent,
            '5': self.showStatistics,
            '6': self.undo,
            '7': self.redo,
            '8': self.listRepo
        }

    def manageStudents(self):
        ManageStudentsMenu(self.controllerWrapper).showMenu()

    def manageAssignments(self):
        ManageAssignmentsMenu(self.controllerWrapper).showMenu()

    def giveAssignments(self):
        AssignMenu(self.controllerWrapper).showMenu()

    def gradeStudent(self):
        studentId = input("Choose student id: ")
        student = self.controllerWrapper.findStudent(studentId)
        print("You are grading the student with name " + student.getName() + " from group " + str(
            student.getGroup()))
        assignmentList = self.controllerWrapper.getStudentUngradedAssignments(studentId)
        if len(assignmentList) == 0:
            print("The student has no ungraded assignments")
            return
        print("\nID - Description - Deadline")
        for assignment in assignmentList:
            print(ManageAssignmentsMenu.assignmentToStr(assignment))
        assignmentId = input("Choose assignment id: ")
        assignment = self.controllerWrapper.findAssignment(assignmentId)
        self.controllerWrapper.assignmentGradable(studentId, assignmentId)
        print(
            "You are grading the assignment with description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
        grade = input("Choose grade: ")
        self.controllerWrapper.grade(studentId, assignmentId, grade)
        print("Assignment was graded")

    def showStatistics(self):
        StatisticsMenu(self.controllerWrapper).showMenu()

    def undo(self):
        if self.controllerWrapper.undo():
            print("Last operation undone")
        else:
            print("No operation left to undo")

    def redo(self):
        if self.controllerWrapper.redo():
            print("Last undo operation reversed")
        else:
            print("No undo operation left to reverse")

    def listRepo(self):
        print("\nSTUDENTS")
        ManageStudentsMenu(self.controllerWrapper).listStudents()
        print("\nGRADES")
        print("\nStudentId - AssignmentId - Grade")
        for grade in self.controllerWrapper.listGrades():
            print(str(grade.getStudentId()) + " - " + str(grade.getAssignmentId()) + " - " + str(grade))
        print("\nASSIGNMENTS")
        ManageAssignmentsMenu(self.controllerWrapper).listAssignments()


class ManageStudentsMenu(Menu):
    menuName = "Manage students"

    def __init__(self, studentController: StudentController):
        super().__init__(studentController)

        self.optionList = [
            "1. List students",
            "2. Add student",
            "3. Remove student",
            "4. Update student",
            "5. List student grades",
            Menu.exitKey + ". Back"
        ]
        self.choiceList = {
            '1': self.listStudents,
            '2': self.addStudent,
            '3': self.removeStudent,
            '4': self.updateStudent,
            '5': self.listStudentGrades
        }

    def listStudents(self):
        studentList = self.controllerWrapper.listStudents()
        print("\nID - Name - Group")
        for student in studentList:
            print(self.studentToStr(student))

    @staticmethod
    def studentToStr(student: Student):
        return str(student.getStudentId()) + " - " + student.getName() + " - " + str(student.getGroup())

    def addStudent(self):
        name = input("Student's name: ")
        group = input("Student's group: ")
        self.controllerWrapper.addStudent(name, group)
        print("Student added")

    def removeStudent(self):
        studentId = input("Student id: ")
        self.controllerWrapper.removeStudent(studentId)
        print("Student removed")

    def updateStudent(self):
        studentId = input("Student id: ")
        student = self.controllerWrapper.findStudent(studentId)
        print("You are modifying the student with name " + student.getName() + " from group " + str(
            student.getGroup()))
        name = input("Student's new name: ")
        group = input("Student's new group: ")
        self.controllerWrapper.updateStudent(studentId, name, group)
        print("Student information updated")

    def listStudentGrades(self):
        studentId = input("Student id: ")
        student = self.controllerWrapper.findStudent(studentId)
        print(student.getName() + "'s grades are:")
        gradeList = self.controllerWrapper.listStudentGrades(studentId)
        if len(gradeList) == 0:
            print("No grades to show")
        else:
            print("Grade - Assignment ID")
            for grade in gradeList:
                print(self.gradeToStr(grade))

    @staticmethod
    def gradeToStr(grade):
        return str(grade) + " - " + str(grade.getAssignmentId())


class ManageAssignmentsMenu(Menu):
    menuName = "Manage assignments"

    def __init__(self, assignmentController: AssignmentController):
        super().__init__(assignmentController)

        self.optionList = [
            "1. List assignments",
            "2. Add assignment",
            "3. Remove assignment",
            "4. Update assignment",
            "5. List assignment grades",
            Menu.exitKey + ". Back"
        ]
        self.choiceList = {
            '1': self.listAssignments,
            '2': self.addAssignment,
            '3': self.removeAssignment,
            '4': self.updateAssignment,
            '5': self.listAssignmentGrades
        }

    def listAssignments(self):
        assignmentList = self.controllerWrapper.listAssignments()
        print("\nID - Description - Deadline")
        for assignment in assignmentList:
            print(self.assignmentToStr(assignment))

    def addAssignment(self):
        description = input("Assignment's description: ")
        deadline = input("Assignment's deadline (format: day.month.year): ")
        self.controllerWrapper.addAssignment(description, deadline)
        print("Assignment added")

    def removeAssignment(self):
        assignmentId = input("Assignment id: ")
        self.controllerWrapper.removeAssignment(assignmentId)
        print("Assignment removed")

    def updateAssignment(self):
        assignmentId = input("Assignment id: ")
        assignment = self.controllerWrapper.findAssignment(assignmentId)
        print(
            "You are modifying the assignment with description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
        description = input("Assignment's new description: ")
        deadline = input("Assignment's new deadline (format: day.month.year): ")
        self.controllerWrapper.updateAssignment(assignmentId, description, deadline)
        print("Assignment information updated")

    @staticmethod
    def assignmentToStr(assignment: Assignment):
        deadline = ManageAssignmentsMenu.dateToStr(assignment.getDeadline())
        return str(
            assignment.getAssignmentId()) + " - " + assignment.getDescription() + " - " + deadline

    @staticmethod
    def dateToStr(parameterDate: date):
        return str(parameterDate.day) + "." + str(parameterDate.month) + "." + str(parameterDate.year)

    def listAssignmentGrades(self):
        assignmentId = input("Assignment id: ")
        assignment = self.controllerWrapper.findAssignment(assignmentId)
        print("List of grades for the assignment with description '" + assignment.getDescription() + "':")
        gradeList = self.controllerWrapper.listAssignmentGrades(assignmentId)
        if len(gradeList) == 0:
            print("No grades to show")
        else:
            print("Grade - Student ID")
            for grade in gradeList:
                print(self.gradeToStr(grade))

    @staticmethod
    def gradeToStr(grade):
        return str(grade) + " - " + str(grade.getStudentId())


class AssignMenu(Menu):
    menuName = "Give assignments"

    def __init__(self, controllerWrapper: ControllerWrapper):
        super().__init__(controllerWrapper)

        self.optionList = [
            "1. Give assignment to student",
            "2. Give assignment to group of students",
            Menu.exitKey + ". Back"
        ]
        self.choiceList = {
            '1': self.assignToStudent,
            '2': self.assignToGroup
        }

    def assignToStudent(self):
        studentId = input("Choose student id: ")
        student = self.controllerWrapper.findStudent(studentId)
        print("You giving an assignment to the student with name " + student.getName() + " from group " + str(
            student.getGroup()))
        assignmentId = input("Choose assignment id: ")
        assignment = self.controllerWrapper.findAssignment(assignmentId)
        print(
            "You are giving the assignment with description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
        self.controllerWrapper.assignToStudent(studentId, assignmentId)
        print("Assignment was given")

    def assignToGroup(self):
        group = input("Choose group: ")
        self.controllerWrapper.checkGroupExistence(group)
        assignmentId = input("Choose assignment id: ")
        assignment = self.controllerWrapper.findAssignment(assignmentId)
        print(
            "You are giving the assignment with description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
        self.controllerWrapper.assignToGroup(group, assignmentId)
        print("Assignments were given")


class StatisticsMenu(Menu):
    menuName = "Statistics menu"

    def __init__(self, controllerWrapper: ControllerWrapper):
        super().__init__(controllerWrapper)

        self.optionList = [
            "1. Students with specified assignment, ordered alphabetically",
            "2. Students with specified assignment, ordered by grade",
            "3. Late students",
            "4. Students sorted descending by average grade",
            "5. Assignments sorted descending by average grade",
            Menu.exitKey + ". Back"
        ]
        self.choiceList = {
            '1': self.studentsSortedAlphabetically,
            '2': self.studentsSortedByGrade,
            '3': self.lateStudents,
            '4': self.studentsSortedByAverage,
            '5': self.assignmentsSortedByAverage
        }

    def studentsSortedAlphabetically(self):
        assignmentId = input("Choose assignment id: ")
        assignment = self.controllerWrapper.findAssignment(assignmentId)
        print(
            "You are viewing the students ordered alphabetically for the assignment with "
            "description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))

        studentList = self.controllerWrapper.getStudentsForAssignmentSortedAlphabetically(assignmentId)
        if len(studentList) == 0:
            print("No students received this assignment")
            return
        print("\nID - Name - Group")
        for student in studentList:
            print(ManageStudentsMenu.studentToStr(student))

    def studentsSortedByGrade(self):
        assignmentId = input("Choose assignment id: ")
        assignment = self.controllerWrapper.findAssignment(assignmentId)
        print(
            "You are viewing the students ordered by grade for the assignment with "
            "description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))

        studentList = self.controllerWrapper.getStudentsForAssignmentSortedByGrade(assignmentId)
        if len(studentList) == 0:
            print("No students received this assignment")
            return
        print("\nID - Name - Group - Grade")
        for student in studentList:
            print(ManageStudentsMenu.studentToStr(student) + " - " +
                  str(self.controllerWrapper.getGrade(student.getStudentId(), assignmentId)))

    def studentsSortedByAverage(self):
        resultList = self.controllerWrapper.getStudentsSortedByAverage()
        if len(resultList) == 0:
            print("No students to show")
            return
        print("\nID - Name - Group - Average grade")
        for pair in resultList:
            print(ManageStudentsMenu.studentToStr(pair[0]) + " - " + (str(pair[1]) if pair[1] != 0 else "No grades"))

    def assignmentsSortedByAverage(self):
        resultList = self.controllerWrapper.getAssignmentsSortedByAverage()
        if len(resultList) == 0:
            print("No assignments to show")
            return
        print("\nID - Description - Deadline - Average Grade")
        for pair in resultList:
            print(ManageAssignmentsMenu.assignmentToStr(pair[0]) + " - " + str(pair[1]))

    def lateStudents(self):
        studentList = self.controllerWrapper.lateStudents()
        if len(studentList) == 0:
            print("No students are late with their assignments")
            return
        print("\nID - Name - Group")
        for student in studentList:
            print(ManageStudentsMenu.studentToStr(student))
