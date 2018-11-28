import random
from copy import copy
from typing import List

from logic.ControllerWrapper import ControllerWrapper
from logic.ValidationUtils import InvalidStudentGroup, ValidationUtils, InvalidStudentId
from model.Student import Student
from logic.ChangesStack import ChangesStack
from repository.Repository import Repository


class StudentController:

    def __init__(self, studentRepository: Repository, controllerWrapper: ControllerWrapper):
        self.__studentRepository = studentRepository
        self.__controllerWrapper = controllerWrapper

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
        ValidationUtils.Student.validateStudent(student)
        self.__studentRepository.addItem(student)
        self.__controllerWrapper.itemAdded(student)

        return student

    def removeStudent(self, studentId: int):
        """
        Removes a student from the repository
        """
        student = self.findStudent(studentId)
        self.__studentRepository.delete(student)
        self.__controllerWrapper.itemRemoved(student)

    def findStudent(self, studentId: int) -> Student:
        """
        Searches a student and returns it if found. Raises InvalidStudentId if not
        """
        student = Student(studentId)
        foundStudent = self.__studentRepository.getItem(student)
        if foundStudent is None:
            raise InvalidStudentId
        return foundStudent

    def updateStudent(self, studentId: int, name: str, group: int):
        """
        Updates the student data
        """

        student = self.findStudent(studentId)
        newStudent = copy(student)
        newStudent.setName(name)
        newStudent.setGroup(group)
        ValidationUtils.Student.validateStudent(newStudent)
        self.__studentRepository.update(newStudent)
        self.__controllerWrapper.itemUpdated(student, newStudent)

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
