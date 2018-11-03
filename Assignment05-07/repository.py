"""
This is the repository module
"""
from typing import Tuple, List

from model import *


class OnDeleteListener:
    # @abstractmethod
    # def onDelete(self, item)
        pass


class Repository(OnDeleteListener):

    def __init__(self):
        self.__students = StudentCollection(self)
        self.__grades = GradeCollection()
        self.__assignments = AssignmentCollection(self)

    def getStudents(self):
        return self.__students

    def getGrades(self):
        return self.__grades

    def getAssignments(self):
        return self.__assignments

    def onDelete(self, item):
        """
        Implements cascade delete for given item
        """
        valid_types = {
            Student: self.onStudentDeleted,
            Assignment: self.onAssignmentDeleted
        }
        if type(item) in valid_types:
            valid_types[type(item)](item)

    def onStudentDeleted(self, student: Student):
        gradeList = self.__grades.getStudentGrades(student)
        for grade in gradeList:
            del self.__grades[grade]

    def onAssignmentDeleted(self, assignment: Assignment):
        gradeList = self.__grades.getAssignmentGrades(assignment)
        for grade in gradeList:
            del self.__grades[grade]


class StudentCollection:
    def __init__(self, onDeleteListener: OnDeleteListener = None):
        self.__students = {}
        self.__idSeed = 0
        self.__length = 0
        self.__onDeleteListener = onDeleteListener

    def addStudent(self, student: Student) -> Student:
        """
        Adds a student with the given information into the collection
        :param student: A student object to be added to the collection (without the studentId)
        :return: The new student object that is contained in the list
        """
        newStudent = Student.copyStudent(self.__idSeed, student)
        self.__students[self.__idSeed] = newStudent
        self.__idSeed += 1
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
        student = self.__students[self.__currentId]
        self.__currentId += 1
        return student

    def __getitem__(self, item: int) -> Student:
        if item in self.__students.keys():
            return self.__students[item]
        return None

    def __delitem__(self, key: Student):
        if key in self.__students.values():
            del self.__students[key.getStudentId()]
            if self.__onDeleteListener is not None:
                self.__onDeleteListener.onDelete(key)
        else:
            raise KeyError("Student is not stored in collection")


class GradeCollection:
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
        if key in self.__grades.values():
            del self.__grades[(key.getStudentId(), key.getAssignmentId())]
        else:
            raise KeyError("Grade is not stored in collection")


class AssignmentCollection:
    def __init__(self, onDeleteListener: OnDeleteListener = None):
        self.__assignments = {}
        self.__idSeed = 0
        self.__length = 0
        self.__onDeleteListener = onDeleteListener

    def addAssignment(self, assignment: Assignment) -> Assignment:
        """
        Adds an assignment with the given information into the collection
        :param assignment: An assignment object to be added to the collection (without the assignmentId)
        :return: The new assignment object that is contained in the list
        """
        newAssignment = Assignment.copyAssignment(self.__idSeed, assignment)
        self.__assignments[self.__idSeed] = newAssignment
        self.__idSeed += 1
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
        assignment = self.__assignments[self.__currentId]
        self.__currentId += 1
        return assignment

    def __getitem__(self, item: int) -> Assignment:
        if item in self.__assignments.keys():
            return self.__assignments[item]
        return None

    def __delitem__(self, key: Assignment):
        if key in self.__assignments.values():
            del self.__assignments[key.getAssignmentId()]
            if self.__onDeleteListener is not None:
                self.__onDeleteListener.onDelete(key)
        else:
            raise KeyError("Assignment is not stored in collection")
