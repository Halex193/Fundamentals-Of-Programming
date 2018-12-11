import datetime
import random
from copy import copy
from typing import List

from lib.CustomComponents import sortList, filterList
from logic.ChangesStack import ChangesStack
from logic.ControllerError import *
from model.Assignment import Assignment
from model.Grade import Grade
from model.Student import Student
from model.Validators import GradeValidator
from repository.Repository import Repository
from repository.RepositoryError import DuplicateItemError


class StudentWithAverageDTO:
    def __init__(self, student: Student, average: float):
        self.__student = student
        self.__average = average

    def getStudent(self) -> Student:
        return self.__student

    def getAverage(self) -> float:
        return self.__average


class AssignmentWithAverageDTO:
    def __init__(self, assignment: Assignment, average: float):
        self.__assignment = assignment
        self.__average = average

    def getAssignment(self) -> Assignment:
        return self.__assignment

    def getAverage(self) -> float:
        return self.__average


class GradeController:

    def __init__(self, studentRepository: Repository, gradeRepository: Repository,
                 assignmentRepository: Repository, currentDate: datetime.date, changesStack: ChangesStack):
        self.__studentRepository = studentRepository
        self.__gradeRepository = gradeRepository
        self.__assignmentRepository = assignmentRepository
        self.__changesStack = changesStack
        self.__currentDate = currentDate

    def findStudent(self, studentId: int) -> Student:
        """
        Searches a student and returns it if found. Raises InvalidStudentId if not
        """
        student = Student(studentId)
        foundStudent = self.__studentRepository.getItem(student)
        if foundStudent is None:
            raise StudentIdNotFound
        return foundStudent

    def findAssignment(self, assignmentId: int) -> Assignment:
        """
        Searches an assignment and returns it if found. Raises InvalidAssignmentId otherwise
        """
        assignment = Assignment(assignmentId)
        foundAssignment = self.__assignmentRepository.getItem(assignment)
        if foundAssignment is None:
            raise AssignmentIdNotFound
        return foundAssignment

    def assignToStudent(self, studentId, assignmentId, newCommit=True) -> Grade:
        """
        Gives an assignment to a student
        """
        self.findStudent(studentId)
        self.findAssignment(assignmentId)
        grade = Grade(studentId, assignmentId)
        self.__gradeRepository.addItem(grade)
        if newCommit:
            self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemAdded(grade))
        if newCommit:
            self.__changesStack.endCommit()
        return grade

    def checkGroupExistence(self, group: int):
        """
        Checks if there are any students within the specified group
        """
        if group not in [student.getGroup() for student in self.__studentRepository.getItems()]:
            raise GroupNotFound

    def assignToGroup(self, group: int, assignmentId: int):
        """
        Gives an assignment to the specified group
        """
        groupStudents = [student for student in self.__studentRepository.getItems() if student.getGroup() == group]
        self.__changesStack.beginCommit()
        for student in groupStudents:
            try:
                self.assignToStudent(student.getStudentId(), assignmentId, newCommit=False)
            except DuplicateItemError:
                pass
        self.__changesStack.endCommit()

    def listStudentGrades(self, studentId: int) -> List[Grade]:
        """
        Lists all the grades for the student with the given ID
        """
        self.findStudent(studentId)
        # return [grade for grade in self.__gradeRepository.getItems() if grade.getStudentId() == studentId]
        return filterList(self.__gradeRepository.getItems(), lambda grade: grade.getStudentId() == studentId)

    def listAssignmentGrades(self, assignmentId) -> List[Grade]:
        """
        Lists all the grades for the assignment with the given ID
        """
        self.findAssignment(assignmentId)
        # return [grade for grade in self.__gradeRepository.getItems() if grade.getAssignmentId() == assignmentId]
        return filterList(self.__gradeRepository.getItems(), lambda grade: grade.getAssignmentId() == assignmentId)

    def findGrade(self, studentId: int, assignmentId: int) -> Grade:
        """
        Finds and returns the grade of a student for a given assignment
        """
        grade = Grade(studentId, assignmentId)
        GradeValidator.validateGrade(grade)
        return self.__gradeRepository.getItem(grade)

    def grade(self, studentId: int, assignmentId: int, grade: int):
        """
        Grades the student at the given assignment
        :param studentId: The ID of the student
        :param assignmentId: The ID of the assignment
        :param grade: The grade of the assignment, an integer between 1 and 10
        :raises InvalidGrade: If an invalid grade is given
        :raises InvalidAssignmentId: If the student has not been given the assignment
        """
        self.findStudent(studentId)
        self.findAssignment(assignmentId)
        gradeObject = self.validateGrading(studentId, assignmentId)
        newGradeObject = copy(gradeObject)
        newGradeObject.setGrade(grade)
        GradeValidator.validateGrade(newGradeObject)
        self.__gradeRepository.updateItem(newGradeObject)

        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(gradeObject))
        self.__changesStack.addChange(ChangesStack.ItemAdded(newGradeObject))
        self.__changesStack.endCommit()

    def getStudentUngradedAssignments(self, studentId: int) -> List[Assignment]:
        """
        Lists the ungraded assignments for the student with the given ID
        """
        self.findStudent(studentId)
        studentGrades = self.listStudentGrades(studentId)
        # studentNoneGrades = [grade for grade in studentGrades if grade.getGrade() is None]
        studentNoneGrades = filterList(studentGrades, lambda grade: grade.getGrade() is None)
        return [self.findAssignment(grade.getAssignmentId()) for grade in studentNoneGrades]

    def validateGrading(self, studentId: int, assignmentId: int) -> Grade:
        """
        Checks if the assignment for a student is gradable
        :returns Grade: If the assignment is gradable,
        returns the Grade object in order to perform the grading operation
        :raises GradeNotFound, GradeAlreadySet: If the assignment is not gradable
        """
        gradeObject = self.findGrade(studentId, assignmentId)
        if gradeObject is None:
            raise GradeNotFound
        elif gradeObject.getGrade() is not None:
            raise GradeAlreadySet
        return gradeObject

    def getStudentsForAssignmentSortedAlphabetically(self, assignmentId: int) -> List[Student]:
        """
        Returns a list of all students who received a given assignment, ordered alphabetically
        """
        grades = self.listAssignmentGrades(assignmentId)
        students = [self.findStudent(grade.getStudentId()) for grade in grades]

        def compareStudentNames(student1, student2):
            name1 = student1.getName()
            name2 = student2.getName()
            if name1 == name2:
                return 0
            if name1 > name2:
                return 1
            return -1

        return sortList(students, compareStudentNames)

    def getStudentsForAssignmentSortedByGrade(self, assignmentId: int) -> List[Student]:
        """
        Returns a list of all students who received a given assignment, ordered by the grade for that assignment
        """
        grades = self.listAssignmentGrades(assignmentId)
        noneGrades = [grade for grade in grades if grade.getGrade() is None]
        givenGrades = [grade for grade in grades if grade.getGrade() is not None]

        def compareGrades(grade1, grade2):
            gradeValue1 = grade1.getGrade()
            gradeValue2 = grade2.getGrade()
            if gradeValue1 == gradeValue2:
                return 0
            if gradeValue1 > gradeValue2:
                return -1
            return 1

        sortedGrades = sortList(givenGrades, compareGrades)
        students = [self.findStudent(grade.getStudentId()) for grade in sortedGrades + noneGrades]
        return students

    def getStudentsSortedByAverage(self) -> List[StudentWithAverageDTO]:
        """
        Returns a list of tuples with the students and their average grades,
        sorted in descending order of the average grade received for all assignments.
        """
        DTOList = []
        students = self.__studentRepository.getItems()
        for student in students:
            sum = 0
            number = 0
            for grade in self.listStudentGrades(student.getStudentId()):
                if grade.getGrade() is not None:
                    sum += grade.getGrade()
                    number += 1
            average = sum / number if number != 0 else 0
            DTOList.append(StudentWithAverageDTO(student, average))

        def compareStudentWithAverageDTO(dto1, dto2):
            average1 = dto1.getAverage()
            average2 = dto2.getAverage()

            if average1 == average2:
                return 0
            if average1 > average2:
                return -1
            return 1

        return sortList(DTOList, compareStudentWithAverageDTO)

    def getAssignmentsSortedByAverage(self) -> List[AssignmentWithAverageDTO]:
        """
        Return a list of tuples consisting of all assignments and their average grades for which there is at least one
        grade, sorted in descending order of the average grade received by all students who received that assignment.
        """
        DTOList = []
        assignments = self.__assignmentRepository.getItems()
        for assignment in assignments:
            sum = 0
            number = 0
            for grade in self.listAssignmentGrades(assignment.getAssignmentId()):
                if grade.getGrade() is not None:
                    sum += grade.getGrade()
                    number += 1
            if number != 0:
                average = sum / number
                DTOList.append(AssignmentWithAverageDTO(assignment, average))

        def compareAssignmentWithAverageDTO(dto1, dto2):
            average1 = dto1.getAverage()
            average2 = dto2.getAverage()

            if average1 == average2:
                return 0
            if average1 > average2:
                return -1
            return 1

        return sortList(DTOList, compareAssignmentWithAverageDTO)

    def getGrade(self, studentId: int, assignmentId: int) -> Grade:
        self.findStudent(studentId)
        self.findAssignment(assignmentId)
        grade = Grade(studentId, assignmentId)
        return self.__gradeRepository.getItem(grade)

    def lateStudents(self) -> List[Student]:
        """
        Returns a list with all students who are late in handing in at least one assignment.
        These are all the students who have an ungraded assignment for which the deadline has passed.
        """
        studentList = []
        for student in self.__studentRepository.getItems():
            ungradedAssignments = self.getStudentUngradedAssignments(student.getStudentId())
            for assignment in ungradedAssignments:
                if self.__currentDate > assignment.getDeadline():
                    studentList.append(student)
                    break
        return studentList

    def listGrades(self) -> List[Grade]:
        return self.__gradeRepository.getItems()

    def addRandomGrades(self, studentNumber: int, assignmentNumber: int, number: int):
        for i in range(number):
            grade = random.randint(0, 10)
            if grade == 0:
                grade = None
            valid = False
            while not valid:
                studentId = random.randint(0, studentNumber - 1)
                assignmentId = random.randint(0, assignmentNumber - 1)
                try:
                    self.__gradeRepository.addItem(Grade(studentId, assignmentId, grade))
                    valid = True
                except DuplicateItemError:
                    pass
