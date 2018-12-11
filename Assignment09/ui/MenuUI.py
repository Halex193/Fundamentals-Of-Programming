"""
This is the menu UI module
"""
import os
from datetime import date

from logic.ControllerError import *
from logic.ControllerWrapper import ControllerWrapper
from model.Assignment import Assignment
from model.Grade import Grade
from model.Student import Student
from model.ValidationError import *
from repository.RepositoryError import *
from ui.UI import UI
from utils.TypeParser import TypeParser


class MenuUI(UI):

    def run(self):
        MainMenu(self.controllerWrapper).showMenu()

    @classmethod
    def handleCustomError(cls, error):

        def getDuplicateItemMessage(genericError):
            if type(genericError) is not DuplicateItemError:
                return ''
            return {
                Student: "Student already exists",
                Grade: "Student was already given this assignment",
                Assignment: "Assignment already exists"
            }[error.getItemType()]

        errorTypes = {
            DuplicateItemError: getDuplicateItemMessage(error),
            InvalidStudentId: "Student id is invalid",
            InvalidStudentGroup: "Student group is invalid",
            InvalidAssignmentId: "Assignment id is invalid",
            InvalidAssignmentDeadline: "Assignment deadline is invalid",
            InvalidGrade: "Grade must be an integer between 0 and 10",
            GroupNotFound: "There is no student with the given group",
            AssignmentIdNotFound: "There is no assignment with the given id",
            StudentIdNotFound: "There is no student with the given id",
            GradeNotFound: "Student was not given the specified assignment",
            GradeAlreadySet: "The student was already graded for the assignment"

        }
        if type(error) in errorTypes:
            print(errorTypes[type(error)])
        else:
            raise error

    @staticmethod
    def gradeToStr(grade) -> str:
        return str(grade.getGrade()) if grade.getGrade() is not None else "No grade"


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
                    except ValidationError as error:
                        MenuUI.handleCustomError(error)
                    except ControllerError as error:
                        MenuUI.handleCustomError(error)
                    except RepositoryError as error:
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
            '8': self.listRepository
        }

    def manageStudents(self):
        ManageStudentsMenu(self.controllerWrapper).showMenu()

    def manageAssignments(self):
        ManageAssignmentsMenu(self.controllerWrapper).showMenu()

    def giveAssignments(self):
        AssignMenu(self.controllerWrapper).showMenu()

    def gradeStudent(self):
        gradeController = self.controllerWrapper.getGradeController()
        studentId = input("Choose student id: ")
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        student = gradeController.findStudent(studentId)
        print("You are grading the student with name " + student.getName() + " from group " + str(
            student.getGroup()))
        assignmentList = gradeController.getStudentUngradedAssignments(studentId)
        if len(assignmentList) == 0:
            print("The student has no ungraded assignments")
            return
        print("\nID - Description - Deadline")
        for assignment in assignmentList:
            print(ManageAssignmentsMenu.assignmentToStr(assignment))
        assignmentId = input("Choose assignment id: ")
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = gradeController.findAssignment(assignmentId)
        gradeController.validateGrading(studentId, assignmentId)
        print(
            "You are grading the assignment with description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
        grade = input("Choose grade: ")
        grade = TypeParser.parseInt(grade, InvalidGrade)
        gradeController.grade(studentId, assignmentId, grade)
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

    def listRepository(self):
        print("\nSTUDENTS")
        ManageStudentsMenu(self.controllerWrapper).listStudents()
        print("\nGRADES")
        print("\nStudentId - AssignmentId - Grade")
        for grade in self.controllerWrapper.getGradeController().listGrades():
            print(grade)
        print("\nASSIGNMENTS")
        ManageAssignmentsMenu(self.controllerWrapper).listAssignments()


class ManageStudentsMenu(Menu):
    menuName = "Manage students"

    def __init__(self, controllerWrapper: ControllerWrapper):
        super().__init__(controllerWrapper)
        self.studentController = controllerWrapper.getStudentController()

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
        studentList = self.studentController.listStudents()
        print("\nID - Name - Group")
        for student in studentList:
            print(self.studentToStr(student))

    @staticmethod
    def studentToStr(student: Student):
        return str(student.getStudentId()) + " - " + student.getName() + " - " + str(student.getGroup())

    def addStudent(self):
        studentId = input("Student's id: ")
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        name = input("Student's name: ")
        group = input("Student's group: ")
        group = TypeParser.parseInt(group, InvalidStudentGroup)
        self.studentController.addStudent(studentId, name, group)
        print("Student added")

    def removeStudent(self):
        studentId = input("Student id: ")
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        self.studentController.removeStudent(studentId)
        print("Student removed")

    def updateStudent(self):
        studentId = input("Student id: ")
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        student = self.studentController.findStudent(studentId)
        print("You are modifying the student with name " + student.getName() + " from group " + str(
            student.getGroup()))
        name = input("Student's new name: ")
        group = input("Student's new group: ")
        group = TypeParser.parseInt(group, InvalidStudentGroup)
        self.studentController.updateStudent(studentId, name, group)
        print("Student information updated")

    def listStudentGrades(self):
        studentId = input("Student id: ")
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        student = self.studentController.findStudent(studentId)
        print(student.getName() + "'s grades are:")
        gradeList = self.controllerWrapper.getGradeController().listStudentGrades(studentId)
        if len(gradeList) == 0:
            print("No grades to show")
        else:
            print("Grade - Assignment ID")
            for grade in gradeList:
                print(self.gradeToStr(grade))

    @staticmethod
    def gradeToStr(grade):
        gradeString = MenuUI.gradeToStr(grade)
        return gradeString + " - " + str(grade.getAssignmentId())


class ManageAssignmentsMenu(Menu):
    menuName = "Manage assignments"

    def __init__(self, controllerWrapper: ControllerWrapper):
        super().__init__(controllerWrapper)
        self.assignmentController = controllerWrapper.getAssignmentController()

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
        assignmentList = self.assignmentController.listAssignments()
        print("\nID - Description - Deadline")
        for assignment in assignmentList:
            print(self.assignmentToStr(assignment))

    def addAssignment(self):
        assignmentId = input("Assignment's id: ")
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        description = input("Assignment's description: ")
        deadline = input("Assignment's deadline (format: day.month.year): ")
        deadline = TypeParser.parseDate(deadline, InvalidAssignmentDeadline)
        self.assignmentController.addAssignment(assignmentId, description, deadline)
        print("Assignment added")

    def removeAssignment(self):
        assignmentId = input("Assignment id: ")
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        self.assignmentController.removeAssignment(assignmentId)
        print("Assignment removed")

    def updateAssignment(self):
        assignmentId = input("Assignment id: ")
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.assignmentController.findAssignment(assignmentId)
        print(
            "You are modifying the assignment with description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
        description = input("Assignment's new description: ")
        deadline = input("Assignment's new deadline (format: day.month.year): ")
        deadline = TypeParser.parseDate(deadline, InvalidAssignmentDeadline)
        self.assignmentController.updateAssignment(assignmentId, description, deadline)
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
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.assignmentController.findAssignment(assignmentId)
        print("List of grades for the assignment with description '" + assignment.getDescription() + "':")
        gradeList = self.controllerWrapper.getGradeController().listAssignmentGrades(assignmentId)
        if len(gradeList) == 0:
            print("No grades to show")
        else:
            print("Grade - Student ID")
            for grade in gradeList:
                print(self.gradeToStr(grade))

    @staticmethod
    def gradeToStr(grade):
        gradeString = MenuUI.gradeToStr(grade)
        return gradeString + " - " + str(grade.getStudentId())


class AssignMenu(Menu):
    menuName = "Give assignments"

    def __init__(self, controllerWrapper: ControllerWrapper):
        super().__init__(controllerWrapper)
        self.gradeController = controllerWrapper.getGradeController()

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
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        student = self.gradeController.findStudent(studentId)
        print("You giving an assignment to the student with name " + student.getName() + " from group " + str(
            student.getGroup()))
        assignmentId = input("Choose assignment id: ")
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.gradeController.findAssignment(assignmentId)
        print(
            "You are giving the assignment with description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
        self.gradeController.assignToStudent(studentId, assignmentId)
        print("Assignment was given")

    def assignToGroup(self):
        group = input("Choose group: ")
        group = TypeParser.parseInt(group, InvalidStudentGroup)
        self.gradeController.checkGroupExistence(group)
        assignmentId = input("Choose assignment id: ")
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.gradeController.findAssignment(assignmentId)
        print(
            "You are giving the assignment with description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
        self.gradeController.assignToGroup(group, assignmentId)
        print("Assignments were given")


class StatisticsMenu(Menu):
    menuName = "Statistics menu"

    def __init__(self, controllerWrapper: ControllerWrapper):
        super().__init__(controllerWrapper)
        self.gradeController = controllerWrapper.getGradeController()

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
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.gradeController.findAssignment(assignmentId)
        print(
            "You are viewing the students ordered alphabetically for the assignment with "
            "description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))

        studentList = self.gradeController.getStudentsForAssignmentSortedAlphabetically(assignmentId)
        if len(studentList) == 0:
            print("No students received this assignment")
            return
        print("\nID - Name - Group")
        for student in studentList:
            print(ManageStudentsMenu.studentToStr(student))

    def studentsSortedByGrade(self):
        assignmentId = input("Choose assignment id: ")
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.gradeController.findAssignment(assignmentId)
        print(
            "You are viewing the students ordered by grade for the assignment with "
            "description '" + assignment.getDescription() +
            "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))

        studentList = self.gradeController.getStudentsForAssignmentSortedByGrade(assignmentId)
        if len(studentList) == 0:
            print("No students received this assignment")
            return
        print("\nID - Name - Group - Grade")
        for student in studentList:
            gradeObject = self.gradeController.getGrade(student.getStudentId(), assignmentId)
            print(ManageStudentsMenu.studentToStr(student) + " - " +
                  MenuUI.gradeToStr(gradeObject))

    def studentsSortedByAverage(self):
        resultList = self.gradeController.getStudentsSortedByAverage()
        if len(resultList) == 0:
            print("No students to show")
            return
        print("\nID - Name - Group - Average grade")
        for dto in resultList:
            averageGrade = (str(dto.getAverage()) if dto.getAverage() != 0 else "No grades")
            print(ManageStudentsMenu.studentToStr(dto.getStudent()) + " - " + averageGrade)

    def assignmentsSortedByAverage(self):
        resultList = self.gradeController.getAssignmentsSortedByAverage()
        if len(resultList) == 0:
            print("No assignments to show")
            return
        print("\nID - Description - Deadline - Average Grade")
        for dto in resultList:
            print(ManageAssignmentsMenu.assignmentToStr(dto.getAssignment()) + " - " + str(dto.getAverage()))

    def lateStudents(self):
        studentList = self.gradeController.lateStudents()
        if len(studentList) == 0:
            print("No students are late with their assignments")
            return
        print("\nID - Name - Group")
        for student in studentList:
            print(ManageStudentsMenu.studentToStr(student))
