import random
from copy import copy
from typing import List

from logic.ChangesStack import ChangesStack
from model.Student import Student
from model.Validators import StudentValidator
from repository.Repository import Repository


class StudentController:

    def __init__(self, studentRepository: Repository, changesStack: ChangesStack):
        self.__studentRepository = studentRepository
        self.__changesStack = changesStack

    def listStudents(self) -> List[Student]:
        """
        Returns a list of students sorted in ascending order by their IDs
        """
        return sorted(self.__studentRepository.getItems(), key=lambda student: student.getStudentId())

    def addStudent(self, studentId: int, name: str, group: int) -> Student:
        """
        Adds a student to the repository
        """
        student = Student(studentId, name, group)
        StudentValidator.validateStudent(student)
        self.__studentRepository.addItem(student)
        self.__changesStack.addChange(ChangesStack.ItemAdded(student), newCommit=True)

        return student

    def removeStudent(self, studentId: int, deleteCallback: function = None):
        """
        Removes a student from the repository
        """
        student = self.findStudent(studentId)
        self.__studentRepository.deleteItem(student)

        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(student))
        if deleteCallback is not None:
            deleteCallback(student)
        else:
            self.__changesStack.endCommit()

    def findStudent(self, studentId: int) -> Student:
        """
        Searches a student and returns it if found. Raises InvalidStudentId if not
        """
        student = Student(studentId)
        foundStudent = self.__studentRepository.getItem(student)
        if foundStudent is None:
            raise StudentIdNotFound
        return foundStudent

    def updateStudent(self, studentId: int, name: str, group: int):
        """
        Updates the student data
        """

        student = self.findStudent(studentId)
        newStudent = copy(student)
        newStudent.setName(name)
        newStudent.setGroup(group)
        StudentValidator.validateStudent(newStudent)
        self.__studentRepository.updateItem(newStudent)
        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(student))
        self.__changesStack.addChange(ChangesStack.ItemAdded(newStudent))
        self.__changesStack.endCommit()

    def addRandomStudents(self, number):
        firstNames = [
            "Richard",
            "Andrew",
            "John",
            "Ray",
            "Ana",
            "Jessica",
            "Bob",
            "Tyler",
            "Lawrence",
            "Kimberly",
            "Scarlet",
            "Diana",
            "Sherlock",
            "Damien",
            "Kathy"
        ]
        lastNames = [
            "Brossard",
            "Crosland",
            "Hutton",
            "Holmes",
            "Hudson",
            "Watson",
            "Heaton",
            "Nelligan",
            "Spears",
            "Redman",
            "Zion",
            "Lambert"
        ]
        groups = [
            911,
            912,
            913,
            914,
            915,
            916,
            917
        ]
        for i in range(number):
            firstName = random.choice(firstNames)
            lastName = random.choice(lastNames)
            group = random.choice(groups)
            self.addStudent(i, firstName + " " + lastName, group)
