from typing import Union, Type

from model.Validators import *
from utils.TypeParser import TypeParser


class CSVConverter:
    """
    A utility class to convert to an from CSV format
    """
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
            TypeParser.parseInt(values[0], InvalidStudentId),
            values[1],
            TypeParser.parseInt(values[2], InvalidStudentGroup)
        )
        StudentValidator.validateStudent(student)
        return student

    @staticmethod
    def __CSVToGrade(csvString: str):
        values = csvString.split(',')
        if values[2] == 'None':
            gradeValue = None
        else:
            gradeValue = TypeParser.parseInt(values[2], InvalidGrade)
        grade = Grade(
            TypeParser.parseInt(values[0], InvalidStudentId),
            TypeParser.parseInt(values[1], InvalidAssignmentId),
            gradeValue
        )
        GradeValidator.validateGrade(grade)
        return grade

    @staticmethod
    def __CSVToAssignment(csvString: str):
        values = csvString.split(',')
        assignment = Assignment(
            TypeParser.parseInt(values[0], InvalidAssignmentId),
            values[1],
            TypeParser.parseDate(values[2], InvalidAssignmentDeadline)
        )
        AssignmentValidator.validateAssignment(assignment)
        return assignment
