"""
Data model module
"""
from datetime import date


class Student:

    def __init__(self, studentId: int, name: str, group: int = None):
        self.__studentId = studentId
        self.__name = name
        self.__group = group

    def getStudentId(self) -> int:
        return self.__studentId

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getGroup(self) -> int:
        return self.__group

    def setGroup(self, group: int):
        self.__group = group

    def __str__(self):
        return self.__name + ((" - " + str(self.__group)) if self.__group is not None else "")

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if self.__studentId == other.__studentId:
            return True
        return False

    @staticmethod
    def copyStudent(studentId, student):
        return Student(studentId, student.__name, student.__group)


class Grade:
    def __init__(self, studentId: int, assignmentId: int, grade: int = None):
        self.__studentId = studentId
        self.__assignmentId = assignmentId
        self.__grade = grade

    def getAssignmentId(self) -> int:
        return self.__assignmentId

    def getStudentId(self) -> int:
        return self.__studentId

    def getGrade(self) -> int:
        return self.__grade

    def setGrade(self, grade: int):
        if self.__grade is not None:
            raise InvalidOperationException('Grade is already set')
        self.__grade = grade

    def __str__(self):
        if self.__grade is None:
            return "No grade"
        return str(self.__grade)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if self.__studentId == other.__studentId and self.__assignmentId == other.__assignmentId:
            return True
        return False


class Assignment:

    def __init__(self, assignmentId: int, description: str, deadline: date):
        self.__assignmentId = assignmentId
        self.__description = description
        self.__deadline = deadline

    def getAssignmentId(self):
        return self.__assignmentId

    def getDescription(self):
        return self.__description

    def setDescription(self, description: str):
        self.__description = description

    def getDeadline(self):
        return self.__deadline

    def setDeadline(self, deadline: date):
        self.__deadline = deadline

    def __str__(self):
        return self.__description + " - " + str(self.__deadline)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if self.__assignmentId == other.__assignmentId:
            return True
        return False

    @staticmethod
    def copyAssignment(assignmentId, assignment):
        return Assignment(assignmentId, assignment.__description, assignment.__deadline)


class InvalidOperationException(Exception):
    pass
