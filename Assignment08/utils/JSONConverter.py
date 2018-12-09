import json

from model.Assignment import Assignment
from model.Grade import Grade
from model.Student import Student
from model.ValidationError import InvalidAssignmentDeadline, InvalidAssignmentId, InvalidStudentId, InvalidStudentGroup
from model.Validators import StudentValidator, GradeValidator, AssignmentValidator
from utils.TypeParser import TypeParser


class JSONConverter:

    @staticmethod
    def convertListToJSON(itemType: type, list) -> str:
        newList = []
        for item in list:
            if itemType is Student:
                newList.append({
                    "studentId": item.getStudentId(),
                    "name": item.getName(),
                    "group": item.getGroup()
                })
            elif itemType is Grade:
                newList.append({
                    "studentId": item.getStudentId(),
                    "assignmentId": item.getAssignmentId(),
                    "grade": item.getGrade()
                })
            elif itemType is Assignment:
                newList.append({
                    "assignmentId": item.getAssignmentId(),
                    "description": item.getDescription(),
                    "deadline": "{:%d.%m.%Y}".format(item.getDeadline())
                })
        return json.dumps(newList, indent=4)

    @staticmethod
    def convertJSONToList(itemType: type, jsonObject):
        list = json.loads(jsonObject)
        newList = []
        newItem = None
        for item in list:
            if itemType is Student:
                newItem = Student(
                    TypeParser.parseInt(item["studentId"], InvalidStudentId),
                    item["name"],
                    TypeParser.parseInt(item["group"], InvalidStudentGroup)
                )
                StudentValidator.validateStudent(newItem)
            elif itemType is Grade:
                newItem = Grade(
                    TypeParser.parseInt(item["studentId"], InvalidStudentId),
                    TypeParser.parseInt(item["assignmentId"], InvalidAssignmentId),
                    item["grade"]
                )
                GradeValidator.validateGrade(newItem)
            elif itemType is Assignment:
                newItem = Assignment(
                    TypeParser.parseInt(item["assignmentId"], InvalidAssignmentId),
                    item["description"],
                    TypeParser.parseDate(item["deadline"], InvalidAssignmentDeadline)
                )
                AssignmentValidator.validateAssignment(newItem)
            newList.append(newItem)

        return newList
