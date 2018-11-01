"""
Validation module
"""
from model import *


class ValidationUtils:

    @staticmethod
    def validStudent(student: Student):
        studentId = student.getStudentId()
        if type(studentId) is not int or studentId < 0:
            return False
        name = student.getName()
        if type(name) is not str:
            return False
        group = student.getGroup()
        if type(group) is not int or group < 0:
            return False
        return True

