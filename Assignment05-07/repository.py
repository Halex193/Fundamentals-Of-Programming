"""
This is the repository module
"""
from typing import Tuple, List

from model import *


class Repository:
    """
    Holds all the program data
    """

    def __init__(self):
        self.__students = StudentCollection()
        self.__grades = GradeCollection()
        self.__assignments = AssignmentCollection()

    def getStudents(self):
        return self.__students

    def getGrades(self):
        return self.__grades

    def getAssignments(self):
        return self.__assignments


class StudentCollection:
    """
    Holds the student objects and provides means of accessing and modifying them
    """

    def __init__(self):
        self.__students = {}
        self.__idSeed = 0
        self.__length = 0

    def addStudent(self, student: Student) -> Student:
        """
        Adds a student with the given information into the collection
        :param student: A student object to be added to the collection (without the studentId)
        :return: The new student object that is contained in the list
        """
        newId = student.getStudentId()
        if student.getStudentId() in self.__students.keys():
            newId = self.__idSeed
            self.__idSeed += 1
        if newId >= self.__idSeed:
            self.__idSeed = newId + 1
        newStudent = Student.copyStudent(newId, student)
        self.__students[newId] = newStudent
        self.__length += 1
        return newStudent

    def __len__(self):
        return self.__length

    def __iter__(self):
        self.__currentId = 0
        return self

    def __next__(self):
        if self.__currentId >= self.__idSeed:
            raise StopIteration
        while self.__currentId not in self.__students.keys():
            self.__currentId += 1
            if self.__currentId >= self.__idSeed:
                raise StopIteration

        student = self.__students[self.__currentId]
        self.__currentId += 1
        return student

    def __getitem__(self, key: int) -> Student:
        if key in self.__students.keys():
            return self.__students[key]
        return None

    def __delitem__(self, key: Student):
        itemId = key.getStudentId()
        if itemId in self.__students.keys():
            del self.__students[itemId]
            self.__length -= 1
        else:
            raise KeyError("Student is not stored in collection")


class GradeCollection:
    """
    Holds the grade objects and provides means of accessing and modifying them
    """

    def __init__(self):
        self.__grades = {}

    def assign(self, student: Student, assignment: Assignment) -> Grade:
        """
        Give an assignment to a student
        :return: The new grade object that is stored in the list
        """

        key = (student.getStudentId(), assignment.getAssignmentId())
        if key in self.__grades.keys():
            raise KeyError('Student was already assigned this assignment')
        newGrade = Grade(student.getStudentId(), assignment.getAssignmentId())
        self.__grades[key] = newGrade
        return newGrade

    def addGrade(self, grade: Grade):
        key = (grade.getStudentId(), grade.getAssignmentId())
        if key not in self.__grades.keys():
            self.__grades[key] = grade

    def getStudentGrades(self, student: Student) -> List[Grade]:
        return [grade for grade in self.__grades.values() if grade.getStudentId() == student.getStudentId()]

    def getAssignmentGrades(self, assignment: Assignment) -> List[Grade]:
        return [grade for grade in self.__grades.values() if grade.getAssignmentId() == assignment.getAssignmentId()]

    def __len__(self):
        return len(self.__grades)

    def __getitem__(self, item: Tuple[int, int]) -> Grade:
        if item in self.__grades.keys():
            return self.__grades[item]
        return None

    def __delitem__(self, key: Grade):
        itemId = (key.getStudentId(), key.getAssignmentId())
        if itemId in self.__grades.keys():
            del self.__grades[itemId]
        else:
            raise KeyError("Grade is not stored in collection")

    def getGradeList(self):
        return [grade for grade in self.__grades.values()]


class AssignmentCollection:
    """
    Holds the assignment objects and provides means of accessing and modifying them
    """

    def __init__(self):
        self.__assignments = {}
        self.__idSeed = 0
        self.__length = 0

    def addAssignment(self, assignment: Assignment) -> Assignment:
        """
        Adds an assignment with the given information into the collection
        :param assignment: An assignment object to be added to the collection (without the assignmentId)
        :return: The new assignment object that is contained in the list
        """
        newId = assignment.getAssignmentId()
        if assignment.getAssignmentId() in self.__assignments.keys():
            newId = self.__idSeed
            self.__idSeed += 1
        if newId >= self.__idSeed:
            self.__idSeed = newId + 1
        newAssignment = Assignment.copyAssignment(newId, assignment)
        self.__assignments[newId] = newAssignment
        self.__length += 1
        return newAssignment

    def __len__(self):
        return self.__length

    def __iter__(self):
        self.__currentId = 0
        return self

    def __next__(self):
        if self.__currentId >= self.__idSeed:
            raise StopIteration
        while self.__currentId not in self.__assignments.keys():
            self.__currentId += 1
            if self.__currentId >= self.__idSeed:
                raise StopIteration
        assignment = self.__assignments[self.__currentId]
        self.__currentId += 1
        return assignment

    def __getitem__(self, item: int) -> Assignment:
        if item in self.__assignments.keys():
            return self.__assignments[item]
        return None

    def __delitem__(self, key: Assignment):
        itemId = key.getAssignmentId()
        if itemId in self.__assignments.keys():
            del self.__assignments[itemId]
            self.__length -= 1
        else:
            raise KeyError("Assignment is not stored in collection")
