"""
Test model module
"""
from unittest import TestCase

from logic.ValidationUtils import *


class TestStudent(TestCase):

    def setUp(self):
        self.student = Student(1, 'Alex', 6)

    def tearDown(self):
        self.student = None

    def testCreate(self):
        student = self.student
        self.assertTrue(student.getStudentId() == 1)
        self.assertTrue(student.getName() == 'Alex')
        self.assertTrue(student.getGroup() == 6)
        self.assertTrue(str(student) == "Alex - 6")
        student = Student(1, 'Alex')
        self.assertTrue(student.getStudentId() == 1)
        self.assertTrue(student.getName() == 'Alex')
        self.assertTrue(student.getGroup() is None)
        self.assertTrue(str(student) == "Alex")
        studentCopy = Student.copyStudent(5, student)
        self.assertTrue(studentCopy.getStudentId() == 5)
        self.assertTrue(studentCopy.getName() == 'Alex')
        self.assertTrue(studentCopy.getGroup() is None)

    def testUpdate(self):
        student = self.student
        student.setName('Other Name')
        self.assertTrue(student.getName() == 'Other Name')
        student.setGroup(8)
        self.assertTrue(student.getGroup() == 8)

    def testEquals(self):
        student = self.student
        self.assertTrue(student == student)
        self.assertTrue(student == Student(1, 'Alex', 6))
        self.assertTrue(student == Student(1, 'Other Name', 7))
        self.assertTrue(student != Student(2, 'Other Name', 7))

    def testValidation(self):
        ValidationUtils.Student.validateStudent(self.student)
        with self.assertRaises(InvalidStudentId):
            ValidationUtils.Student.validateStudent(Student(-3, 'Name', 8))
        with self.assertRaises(InvalidStudentId):
            ValidationUtils.Student.validateStudent(Student('str', 'Name', 8))
        with self.assertRaises(InvalidStudentName):
            ValidationUtils.Student.validateStudent(Student(3, 8, 8))
        with self.assertRaises(InvalidStudentGroup):
            ValidationUtils.Student.validateStudent(Student(3, 'Name', -8))
        with self.assertRaises(InvalidStudentGroup):
            ValidationUtils.Student.validateStudent(Student(3, 'Name', 'str'))


class TestGrade(TestCase):

    def setUp(self):
        self.grade = Grade(1, 2, 10)

    def tearDown(self):
        self.grade = None

    def testCreate(self):
        grade = self.grade
        self.assertTrue(grade.getStudentId() == 1)
        self.assertTrue(grade.getAssignmentId() == 2)
        self.assertTrue(grade.getGrade() == 10)
        self.assertTrue(Grade(3, 4).getGrade() is None)
        self.assertTrue(str(grade) == "10")
        self.assertTrue(str(Grade(3, 4)) == "No grade")

    def testUpdate(self):
        grade = Grade(1, 4)
        grade.setGrade(14)
        self.assertTrue(grade.getGrade() == 14)
        with self.assertRaises(InvalidOperationException):
            grade.setGrade(12)

    def testEquals(self):
        grade = self.grade
        self.assertTrue(grade == grade)
        self.assertTrue(grade == Grade(1, 2, 10))
        self.assertTrue(grade == Grade(1, 2, 7))
        self.assertTrue(grade != Grade(1, 3, 7))
        self.assertTrue(grade != Grade(3, 2, 7))


class TestAssignment(TestCase):

    def setUp(self):
        self.assignment = Assignment(1, 'Project', date(2018, 7, 11))

    def tearDown(self):
        self.assignment = None

    def testCreate(self):
        assignment = self.assignment
        self.assertTrue(assignment.getAssignmentId() == 1)
        self.assertTrue(assignment.getDescription() == 'Project')
        self.assertTrue(assignment.getDeadline() == date(2018, 7, 11))
        self.assertTrue(str(assignment) == "Project - 2018-07-11")

    def testUpdate(self):
        assignment = self.assignment
        assignment.setDescription('Other description')
        self.assertTrue(assignment.getDescription() == 'Other description')
        assignment.setDeadline(date(2017, 9, 13))
        self.assertTrue(assignment.getDeadline() == date(2017, 9, 13))

    def testEquals(self):
        assignment = self.assignment
        self.assertTrue(assignment == assignment)
        self.assertTrue(assignment == Assignment(1, 'Project', date(2018, 7, 11)))
        self.assertTrue(assignment == Assignment(1, 'Other Project', date(2020, 5, 9)))
        self.assertTrue(assignment != Assignment(3, 'Other Project', date(2020, 5, 9)))

    def testValidation(self):
        ValidationUtils.Assignment.validateAssignment(self.assignment)
        sampleDate = date(2018, 7, 8)
        with self.assertRaises(InvalidAssignmentId):
            ValidationUtils.Assignment.validateAssignment(Assignment(-3, 'Desc', sampleDate))
        with self.assertRaises(InvalidAssignmentId):
            ValidationUtils.Assignment.validateAssignment(Assignment('str', 'Desc', sampleDate))
        with self.assertRaises(InvalidAssignmentDescription):
            ValidationUtils.Assignment.validateAssignment(Assignment(3, 8, sampleDate))
        with self.assertRaises(InvalidAssignmentDeadline):
            ValidationUtils.Assignment.validateAssignment(Assignment(3, 'Desc', -8))
        with self.assertRaises(InvalidAssignmentDeadline):
            ValidationUtils.Assignment.validateAssignment(Assignment(3, 'Desc', 'str'))
