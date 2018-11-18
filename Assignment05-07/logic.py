"""
This is the logic module
"""
from datetime import datetime

from repository import *
from validation import *
from typing import *


class ChangesHandler:
    # @abstractmethod
    # def handleChanges(self, changes):
    pass


class DuplicateAssignment(CustomError):
    pass


class LogicComponent(ChangesHandler):
    """
    Provides all the logic functions of the software
    """

    def __init__(self, repository: Repository, currentDate: date):
        self.__repository = repository
        self.__students: StudentCollection = repository.getStudents()
        self.__grades: GradeCollection = repository.getGrades()
        self.__assignments: AssignmentCollection = repository.getAssignments()
        self.__changesStack: ChangesStack = ChangesStack(self)
        self.currentDate = currentDate

    def handleChanges(self, changes):
        pass

    def populateRepository(self):
        """
        Adds default data to the repository
        """
        studentList = [
            self.__students.addStudent(Student(0, 'Andrew', 915)),
            self.__students.addStudent(Student(0, 'Richard', 915)),
            self.__students.addStudent(Student(0, 'John', 917)),
            self.__students.addStudent(Student(0, 'Hori', 917))
        ]
        assignmentList = [
            self.__assignments.addAssignment(Assignment(0, 'Assignment 01', date(2018, 10, 10))),
            self.__assignments.addAssignment(Assignment(0, 'Assignment 02', date(2018, 10, 17))),
            self.__assignments.addAssignment(Assignment(0, 'Assignment 03-04', date(2018, 10, 31))),
            self.__assignments.addAssignment(Assignment(0, 'Assignment 05-07', date(2018, 11, 28)))
        ]

        self.__grades.assign(studentList[0], assignmentList[1]).setGrade(10)
        self.__grades.assign(studentList[0], assignmentList[3])
        self.__grades.assign(studentList[1], assignmentList[1]).setGrade(5)
        self.__grades.assign(studentList[1], assignmentList[2]).setGrade(4)
        self.__grades.assign(studentList[2], assignmentList[2])
        self.__grades.assign(studentList[2], assignmentList[3]).setGrade(9)
        self.__grades.assign(studentList[3], assignmentList[1])

    # Manage Students menu
    def listStudents(self) -> List[Student]:
        """
        Returns a list of students sorted in ascending order by their IDs
        """
        return sorted([student for student in self.__students], key=lambda student: student.getStudentId())

    def addStudent(self, name: str, group: str) -> Student:
        """
        Adds a student to the repository
        """
        group = self.parseInt(group, InvalidStudentGroup)
        student = Student(0, name, group)
        ValidationUtils.Student.validateStudent(student)
        return self.__students.addStudent(student)

    @staticmethod
    def parseInt(string: str, errorType: type) -> int:
        """
        Parses a number to an integer. If the conversion fails, raises the specified exception
        """
        try:
            return int(string)
        except ValueError:
            raise errorType()

    def removeStudent(self, studentId: str):
        """
        Removes a student from the repository
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        student = self.findStudent(studentId)
        del self.__students[student]

    def findStudent(self, studentId) -> Student:
        """
        Searches a student and returns it if found. Raises InvalidStudentId if not
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        if studentId not in [student.getStudentId() for student in self.__students]:
            raise InvalidStudentId
        else:
            return self.__students[studentId]

    def updateStudent(self, studentId, name: str, group: str):
        """
        Updates the student data
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        group = self.parseInt(group, InvalidStudentGroup)
        ValidationUtils.Student.validateStudent(Student(0, name, group))
        student = self.findStudent(studentId)
        student.setName(name)
        student.setGroup(group)

    # Manage Assignments Menu
    def listAssignments(self) -> List[Assignment]:
        """
        Returns a list of assignments sorted in ascending order by their IDs
        """
        return sorted([assignment for assignment in self.__assignments],
                      key=lambda assignment: assignment.getAssignmentId())

    def addAssignment(self, description: str, deadline: str) -> Assignment:
        """
        Adds a assignment to the repository
        """
        deadline = self.parseDate(deadline, InvalidAssignmentDeadline)
        assignment = Assignment(0, description, deadline)
        ValidationUtils.Assignment.validateAssignment(assignment)
        return self.__assignments.addAssignment(assignment)

    @staticmethod
    def parseDate(string: str, errorType: type) -> date:
        """
        Parses a string to a date. Valid format: day.month.year . If the conversion fails, raises the specified exception
        """
        try:
            symbols = string.split('.')
            if len(symbols) != 3:
                raise errorType()
            day = int(symbols[0])
            month = int(symbols[1])
            year = int(symbols[2])
            return date(year, month, day)
        except ValueError:
            raise errorType()

    def removeAssignment(self, assignmentId: str):
        """
        Removes an assignment from the repository
        """
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.findAssignment(assignmentId)
        del self.__assignments[assignment]

    def findAssignment(self, assignmentId) -> Assignment:
        """
        Searches an assignment and returns it if found. Raises InvalidAssignmentId otherwise
        """
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        if assignmentId not in [assignment.getAssignmentId() for assignment in self.__assignments]:
            raise InvalidAssignmentId
        else:
            return self.__assignments[assignmentId]

    def updateAssignment(self, assignmentId, description: str, deadline: str):
        """
        Updates the assignment data
        """
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        deadline = self.parseDate(deadline, InvalidAssignmentDeadline)
        ValidationUtils.Assignment.validateAssignment(Assignment(0, description, deadline))
        assignment = self.findAssignment(assignmentId)
        assignment.setDescription(description)
        assignment.setDeadline(deadline)

    # Give assignments menu
    def assignToStudent(self, studentId, assignmentId) -> Grade:
        """
        Gives an assignment to a student
        """
        student = self.findStudent(studentId)
        assignment = self.findAssignment(assignmentId)
        try:
            return self.__grades.assign(student, assignment)
        except KeyError:
            raise DuplicateAssignment

    def checkGroupExistence(self, group: str):
        """
        Checks if there are any students within the specified group
        """
        group = self.parseInt(group, InvalidStudentGroup)
        if group not in [student.getGroup() for student in self.__students]:
            raise InvalidStudentGroup

    def assignToGroup(self, group: str, assignmentId: str):
        """
        Gives an assignment to the specified group
        """
        group = self.parseInt(group, InvalidStudentGroup)
        groupStudents = [student for student in self.__students if student.getGroup() == group]
        for student in groupStudents:
            try:
                self.assignToStudent(student.getStudentId(), assignmentId)
            except DuplicateAssignment:
                pass

    def listStudentGrades(self, studentId) -> List[Grade]:
        """
        Lists all the grades for the student with the given ID
        """
        student = self.findStudent(studentId)
        return self.__grades.getStudentGrades(student)

    def listAssignmentGrades(self, assignmentId) -> List[Grade]:
        """
        Lists all the grades for the assignment with the given ID
        """
        assignment = self.findAssignment(assignmentId)
        return self.__grades.getAssignmentGrades(assignment)

    def grade(self, studentId: str, assignmentId: str, grade: str):
        """
        Grades the student at the given assignment
        :param studentId: The ID of the student
        :param assignmentId: The ID of the assignment
        :param grade: THe grade of the assignment, an integer between 1 and 10
        :raises InvalidGrade: If an invalid grade is given
        :raises InvalidAssignmentId: If the student has not been given the assignment
        """
        self.findStudent(studentId)
        self.findAssignment(assignmentId)
        grade = self.parseInt(grade, InvalidGrade)
        if grade < 1 or grade > 10:
            raise InvalidGrade
        gradeObject = self.findGrade(studentId, assignmentId)
        if gradeObject is None or gradeObject.getGrade() is not None:
            raise InvalidAssignmentId
        gradeObject.setGrade(grade)

    def getStudentUngradedAssignments(self, studentId) -> List[Assignment]:
        """
        Lists the ungraded assignments for the student with the given ID
        """
        student = self.findStudent(studentId)
        studentGrades = self.__grades.getStudentGrades(student)
        studentNoneGrades = [grade for grade in studentGrades if grade.getGrade() is None]
        return [self.findAssignment(grade.getAssignmentId()) for grade in studentNoneGrades]

    def assignmentGradable(self, studentId: str, assignmentId: str):
        """
        Checks if the assignment for a student is gradable
        :raises InvalidAssignmentId: If the assignment is not gradable
        """
        gradeObject = self.findGrade(studentId, assignmentId)
        if gradeObject is None or gradeObject.getGrade() is not None:
            raise InvalidAssignmentId

    def findGrade(self, studentId: str, assignmentId: str) -> Grade:
        """
        Finds and returns the grade of a student for a given assignment
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        return self.__grades[studentId, assignmentId]

    def getStudentsForAssignmentSortedAlphabetically(self, assignmentId) -> List[Student]:
        """
        Returns a list of all students who received a given assignment, ordered alphabetically
        """
        grades = self.listAssignmentGrades(assignmentId)
        students = [self.findStudent(grade.getStudentId()) for grade in grades]
        return sorted(students, key=lambda student: student.getName())

    def getStudentsForAssignmentSortedByGrade(self, assignmentId) -> List[Student]:
        """
        Returns a list of all students who received a given assignment, ordered by the grade for that assignment
        """
        grades = self.listAssignmentGrades(assignmentId)
        noneGrades = [grade for grade in grades if grade.getGrade() is None]
        givenGrades = [grade for grade in grades if grade.getGrade() is not None]
        sortedGrades = sorted(givenGrades, key=lambda grade: grade.getGrade(), reverse=True)
        students = [self.findStudent(grade.getStudentId()) for grade in sortedGrades + noneGrades]
        return students

    def getStudentsSortedByAverage(self) -> List[Tuple[Student, float]]:
        """
        Returns a list of tuples with the students and their average grades,
        sorted in descending order of the average grade received for all assignments.
        """
        studentList = []
        students = self.__students
        for student in students:
            sum = 0
            number = 0
            for grade in self.__grades.getStudentGrades(student):
                if grade.getGrade() is not None:
                    sum += grade.getGrade()
                    number += 1
            average = sum / number if number != 0 else 0
            studentList.append((student, average))
        return sorted(studentList, key=lambda pair: pair[1], reverse=True)

    def getAssignmentsSortedByAverage(self) -> List[Tuple[Assignment, float]]:
        """
        Return a list of tuples consisting of all assignments and their average grades for which there is at least one
        grade, sorted in descending order of the average grade received by all students who received that assignment.
        """
        assignmentList = []
        assignments = self.__assignments
        for assignment in assignments:
            sum = 0
            number = 0
            for grade in self.__grades.getAssignmentGrades(assignment):
                if grade.getGrade() is not None:
                    sum += grade.getGrade()
                    number += 1
            if number != 0:
                average = sum / number
                assignmentList.append((assignment, average))
        return sorted(assignmentList, key=lambda pair: pair[1], reverse=True)

    def getGrade(self, studentId, assignmentId):
        student = self.findStudent(studentId)
        assignment = self.findAssignment(assignmentId)
        return self.__grades[student.getStudentId(), assignment.getAssignmentId()]

    def lateStudents(self) -> List[Student]:
        """
        Returns a list with all students who are late in handing in at least one assignment.
        These are all the students who have an ungraded assignment for which the deadline has passed.
        """
        studentList = []
        for student in self.listStudents():
            ungradedAssignments = self.getStudentUngradedAssignments(student.getStudentId())
            for assignment in ungradedAssignments:
                if self.currentDate > assignment.getDeadline():
                    studentList.append(student)
                    break
        return studentList


class ChangesStack:
    """
    The stack of changes committed to the repository
    """

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
