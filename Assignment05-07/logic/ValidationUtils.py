"""
Validation module
"""
from datetime import date

from model.Assignment import Assignment
from model.Student import Student


class ValidationError(Exception):
    pass


class InvalidStudentId(ValidationError):
    pass


class InvalidStudentName(ValidationError):
    pass


class InvalidStudentGroup(ValidationError):
    pass


class InvalidAssignmentId(ValidationError):
    pass


class InvalidAssignmentDescription(ValidationError):
    pass


class InvalidAssignmentDeadline(ValidationError):
    pass


class InvalidGrade(ValidationError):
    pass


class ValidationUtils:
    """
    Provides means of validating program data
    """

    class Student:
        @staticmethod
        def validateStudent(student: Student):
            ValidationUtils.Student.validateId(student.getStudentId())
            ValidationUtils.Student.validateName(student.getName())
            ValidationUtils.Student.validateGroup(student.getGroup())

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

    class Assignment:
        @staticmethod
        def validateAssignment(assignment: Assignment):
            ValidationUtils.Assignment.validateId(assignment.getAssignmentId())
            ValidationUtils.Assignment.validateDescription(assignment.getDescription())
            ValidationUtils.Assignment.validateDeadline(assignment.getDeadline())

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
