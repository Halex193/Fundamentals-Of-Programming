from typing import Union, Type

from model.Assignment import Assignment
from model.Grade import Grade
from model.Student import Student
from model.ValidationUtils import *


class CSVConverter:

    @staticmethod
    def convertItemToCSV(item: Union[Student, Grade, Assignment]):
        toCSV = {
            Student: CSVConverter.__studentToCSV,
            Grade: CSVConverter.__gradeToCSV,
            Assignment: CSVConverter.__assignmentToCSV
        }
        return toCSV[type(item)](item)

    @staticmethod
    def convertCSVToItem(itemType: Type[Union[Student, Grade, Assignment]], csvString: str):
        toItem = {
            Student: CSVConverter.__CSVToStudent,
            Grade: CSVConverter.__CSVToGrade,
            Assignment: CSVConverter.__CSVToAssignment
        }
        return toItem[itemType](csvString)

    @staticmethod
    def __studentToCSV(student: Student):
        return "{:d},{},{}".format(
            student.getStudentId(),
            student.getName(),
            student.getGroup()
        )

    @staticmethod
    def __gradeToCSV(grade: Grade):
        return "{:d},{:d},{}".format(
            grade.getStudentId(),
            grade.getAssignmentId(),
            grade.getGrade()
        )

    @staticmethod
    def __assignmentToCSV(assignment: Assignment):
        return "{:d},{},{:%d.%m.%Y}".format(
            assignment.getAssignmentId(),
            assignment.getDescription(),
            assignment.getDeadline()
        )

    @staticmethod
    def __CSVToStudent(csvString: str):
        values = csvString.split(',')
        student = Student(
            ValidationUtils.parseInt(values[0], InvalidStudentId),
            values[1],
            ValidationUtils.parseInt(values[2], InvalidStudentGroup)
        )
        ValidationUtils.Student.validateStudent(student)
        return student

    @staticmethod
    def __CSVToGrade(csvString: str):
        values = csvString.split(',')
        if values[2] == 'None':
            gradeValue = None
        else:
            gradeValue = ValidationUtils.parseInt(values[2], InvalidGrade)
        grade = Grade(
            ValidationUtils.parseInt(values[0], InvalidStudentId),
            ValidationUtils.parseInt(values[1], InvalidAssignmentId),
            gradeValue
        )
        # ValidationUtils.Grade.validateStudent(grade)
        # TODO validate Grade
        return grade

    @staticmethod
    def __CSVToAssignment(csvString: str):
        values = csvString.split(',')
        assignment = Assignment(
            ValidationUtils.parseInt(values[0], InvalidAssignmentId),
            values[1],
            ValidationUtils.parseDate(values[2], InvalidAssignmentDeadline)
        )
        ValidationUtils.Assignment.validateAssignment(assignment)
        return assignment
