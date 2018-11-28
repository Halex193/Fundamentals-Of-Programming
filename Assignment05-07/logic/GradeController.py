# TODO finish this
import datetime
from random import random

from logic.ControllerWrapper import ControllerWrapper
from logic.ValidationUtils import InvalidStudentId, InvalidAssignmentId
from model.Assignment import Assignment
from model.Grade import Grade
from model.Student import Student
from repository.Repository import Repository


class GradeController:

    def __init__(self, studentRepository: Repository, gradeRepository: Repository,
                 assignmentRepository: Repository, currentDate: datetime.date, controllerWrapper: ControllerWrapper):
        self.__studentRepository = studentRepository
        self.__gradeRepository = gradeRepository
        self.__assignmentRepository = assignmentRepository
        self.__controllerWrapper = controllerWrapper
        self.__currentDate = currentDate

    def findStudent(self, studentId: int) -> Student:
        """
        Searches a student and returns it if found. Raises InvalidStudentId if not
        """
        student = Student(studentId)
        foundStudent = self.__studentRepository.getItem(student)
        if foundStudent is None:
            raise InvalidStudentId
        return foundStudent

    def findAssignment(self, assignmentId: int) -> Assignment:
        """
        Searches an assignment and returns it if found. Raises InvalidAssignmentId otherwise
        """
        assignment = Assignment(assignmentId)
        foundAssignment = self.__assignmentRepository.getItem(assignment)
        if foundAssignment is None:
            raise InvalidAssignmentId
        return foundAssignment

    def assignToStudent(self, studentId, assignmentId, newCommit=True) -> Grade:
        """
        Gives an assignment to a student
        """
        self.findStudent(studentId)
        self.findAssignment(assignmentId)
        grade = Grade(studentId, assignmentId)
        self.__gradeRepository.addItem(grade)
        # TODO think about this
        if newCommit:
            self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemAdded(newGrade))
        if newCommit:
            self.__changesStack.endCommit()
        return newGrade

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
        self.__changesStack.beginCommit()
        for student in groupStudents:
            try:
                self.assignToStudent(student.getStudentId(), assignmentId, newCommit=False)
            except DuplicateAssignment:
                pass
        self.__changesStack.endCommit()

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
        :param grade: The grade of the assignment, an integer between 1 and 10
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
        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(gradeObject))
        gradeObject.setGrade(grade)
        self.__changesStack.addChange(ChangesStack.ItemAdded(gradeObject))
        self.__changesStack.endCommit()

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

    def listGrades(self):
        return self.__grades.getGradeList()

    def addRandomGrades(self, studentNumber, assignmentNumber, number):
        for i in range(number):
            studentId = random.randint(0, studentNumber - 1)
            assignmentId = random.randint(0, assignmentNumber - 1)
            grade = random.randint(0, 10)
            if grade == 0:
                grade = None
            self.__grades.addGrade(Grade(studentId, assignmentId, grade))
