"""
Validation module
"""
from datetime import date

from model.Assignment import Assignment
from model.Grade import Grade
from model.Student import Student
from model.ValidationError import *


class StudentValidator:

    @staticmethod
    def validateStudent(student: Student):
        StudentValidator.validateId(student.getStudentId())
        StudentValidator.validateName(student.getName())
        StudentValidator.validateGroup(student.getGroup())

    @staticmethod
    def validateId(studentId):
        if type(studentId) is not int or studentId < 0:
            raise InvalidStudentId

    @staticmethod
    def validateName(name):
        if type(name) is not str:
            raise InvalidStudentName

    @staticmethod
    def validateGroup(group):
        if type(group) is not int or group < 0:
            raise InvalidStudentGroup


class AssignmentValidator:

    @staticmethod
    def validateAssignment(assignment: Assignment):
        AssignmentValidator.validateId(assignment.getAssignmentId())
        AssignmentValidator.validateDescription(assignment.getDescription())
        AssignmentValidator.validateDeadline(assignment.getDeadline())

    @staticmethod
    def validateId(studentId):
        if type(studentId) is not int or studentId < 0:
            raise InvalidAssignmentId

    @staticmethod
    def validateDescription(description):
        if type(description) is not str:
            raise InvalidAssignmentDescription

    @staticmethod
    def validateDeadline(deadline):
        if type(deadline) is not date:
            raise InvalidAssignmentDeadline


class GradeValidator:

    @staticmethod
    def validateGrade(grade: Grade):
        StudentValidator.validateId(grade.getStudentId())
        AssignmentValidator.validateId(grade.getAssignmentId())
        GradeValidator.validateGradeNumber(grade.getGrade())

    @staticmethod
    def validateGradeNumber(gradeNumber):
        if gradeNumber is None:
            return
        if type(gradeNumber) is not int or gradeNumber < 1 or gradeNumber > 10:
            raise InvalidGrade
