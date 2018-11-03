"""
Test model module
"""
from unittest import TestCase

from validation import *
from model import *


class TestStudent(TestCase):

    def setUp(self):
        self.student = Student(1, 'Alex', 6)

    def testCreate(self):
        student = self.student
        assert student.getStudentId() == 1
        assert student.getName() == 'Alex'
        assert student.getGroup() == 6
        assert str(student) == "Alex - 6"
        student = Student(1, 'Alex')
        assert student.getStudentId() == 1
        assert student.getName() == 'Alex'
        assert student.getGroup() is None
        assert str(student) == "Alex"
        studentCopy = Student.copyStudent(5, student)
        assert studentCopy.getStudentId() == 5
        assert studentCopy.getName() == 'Alex'
        assert studentCopy.getGroup() is None

    def testUpdate(self):
        student = self.student
        student.setName('Other Name')
        assert student.getName() == 'Other Name'
        student.setGroup(8)
        assert student.getGroup() == 8

    def testEquals(self):
        student = self.student
        assert student == student
        assert student == Student(1, 'Alex', 6)
        assert student == Student(1, 'Other Name', 7)
        assert student != Student(2, 'Other Name', 7)

    # def testValidation(self):
    #     assert ValidationUtils.validateStudent(self.student)
    #     assert not ValidationUtils.validateStudent(Student(-3, 'Name', 8))
    #     assert not ValidationUtils.validateStudent(Student('str', 'Name', 8))
    #     assert not ValidationUtils.validateStudent(Student(3, 8, 8))
    #     assert not ValidationUtils.validateStudent(Student(3, 'Name', -8))
    #     assert not ValidationUtils.validateStudent(Student(3, 'Name', 'str'))


class TestGrade(TestCase):

    def setUp(self):
        self.grade = Grade(1, 2, 10)

    def testCreate(self):
        grade = self.grade
        assert grade.getStudentId() == 1
        assert grade.getAssignmentId() == 2
        assert grade.getGrade() == 10
        assert Grade(3, 4).getGrade() is None
        assert str(grade) == "10"
        assert str(Grade(3, 4)) == "No grade"

    def testUpdate(self):
        grade = Grade(1, 4)
        grade.setGrade(14)
        assert grade.getGrade() == 14
        self.assertRaises(InvalidOperationException, grade.setGrade, 12)

    def testEquals(self):
        grade = self.grade
        assert grade == grade
        assert grade == Grade(1, 2, 10)
        assert grade == Grade(1, 2, 7)
        assert grade != Grade(1, 3, 7)
        assert grade != Grade(3, 2, 7)


class TestAssignment(TestCase):

    def setUp(self):
        self.assignment = Assignment(1, 'Project', date(2018, 7, 11))

    def testCreate(self):
        assignment = self.assignment
        assert assignment.getAssignmentId() == 1
        assert assignment.getDescription() == 'Project'
        assert assignment.getDeadline() == date(2018, 7, 11)
        assert str(assignment) == "Project - 2018-07-11"

    def testUpdate(self):
        assignment = self.assignment
        assignment.setDescription('Other description')
        assert assignment.getDescription() == 'Other description'
        assignment.setDeadline(date(2017, 9, 13))
        assert assignment.getDeadline() == date(2017, 9, 13)

    def testEquals(self):
        assignment = self.assignment
        assert assignment == assignment
        assert assignment == Assignment(1, 'Project', date(2018, 7, 11))
        assert assignment == Assignment(1, 'Other Project', date(2020, 5, 9))
        assert assignment != Assignment(3, 'Other Project', date(2020, 5, 9))
