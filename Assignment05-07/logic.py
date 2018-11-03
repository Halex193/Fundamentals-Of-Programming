"""
This is the logic module
"""

from repository import *
from model import *
from validation import *
from typing import *


class ChangesHandler:
    # @abstractmethod
    # def handleChanges(self, changes):
    pass


class LogicComponent(ChangesHandler):

    def __init__(self, repository: Repository):
        self.__repository = repository
        self.__students: StudentCollection = repository.getStudents()
        self.__grades: GradeCollection = repository.getGrades()
        self.__assignments: AssignmentCollection = repository.getAssignments()
        self.__changesStack: ChangesStack = ChangesStack(self)
        self.populateRepository()

    def handleChanges(self, changes):
        pass

    def populateRepository(self):
        studentList = [
            self.__students.addStudent(Student(0, 'Andrew', 1)),
            self.__students.addStudent(Student(0, 'Richard', 1)),
            self.__students.addStudent(Student(0, 'John', 5)),
            self.__students.addStudent(Student(0, 'Michaela', 5))
        ]
        assignmentList = [
            self.__assignments.addAssignment(Assignment(0, 'Project 1', date(2018, 9, 8))),
            self.__assignments.addAssignment(Assignment(0, 'Project 2', date(2018, 10, 8))),
            self.__assignments.addAssignment(Assignment(0, 'Project 3', date(2018, 11, 8))),
            self.__assignments.addAssignment(Assignment(0, 'Project 4', date(2018, 12, 8)))
        ]

        self.__grades.assign(studentList[0], assignmentList[1])
        self.__grades.assign(studentList[0], assignmentList[3])
        self.__grades.assign(studentList[1], assignmentList[1])
        self.__grades.assign(studentList[1], assignmentList[2])
        self.__grades.assign(studentList[2], assignmentList[2])
        self.__grades.assign(studentList[2], assignmentList[3])
        self.__grades.assign(studentList[3], assignmentList[1])

    def listStudents(self):
        return sorted([student for student in self.__students], key=lambda student: student.getStudentId())

    def addStudent(self, name: str, group: str):
        group = self.parse_int(group, InvalidStudentGroup)
        student = Student(0, name, group)
        ValidationUtils.Student.validateStudent(student)
        self.__students.addStudent(student)

    @staticmethod
    def parse_int(string: str, errorType: type) -> int:
        try:
            return int(string)
        except ValueError:
            raise errorType()

    def removeStudent(self, studentId):
        studentId = self.parse_int(studentId, InvalidStudentId)
        if studentId not in [student.getStudentId() for student in self.__students]:
            raise InvalidStudentId
        del self.__students[Student(studentId, '')]


class ChangesStack:

    def __init__(self, changesHandler):
        self.__changesStack = []
        self.__changesHandler = changesHandler

    def beginCommit(self):
        pass

    def endCommit(self):
        pass

    def addChange(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass
