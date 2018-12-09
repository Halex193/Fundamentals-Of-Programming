from typing import List, Tuple

import mysql.connector

from model.Assignment import Assignment
from model.Grade import Grade
from model.Student import Student
from model.ValidationError import InvalidAssignmentDeadline
from repository.RepositoryError import RepositoryError
from utils.TypeParser import TypeParser


class MySQLConnector:
    """
    Utility class for using MySQL-backed repositories
    """
    def __init__(self):
        try:
            self.__connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="Assignment08"
            )
        except Exception:
            raise RepositoryError("Database connection refused")

    def getConnection(self):
        return self.__connection

    @staticmethod
    def idCheckString(item):
        itemType: type = type(item)
        if itemType is Student:
            return "studentId = '{}'".format(item.getStudentId())
        if itemType is Grade:
            return "studentID = '{}' AND assignmentId = '{}'".format(item.getStudentId(), item.getAssignmentId())
        if itemType is Assignment:
            return "assignmentId = '{}'".format(item.getAssignmentId())

    @staticmethod
    def valuesString(item):
        itemType: type = type(item)
        if itemType is Student:
            return "'{}', '{}', '{}'".format(item.getStudentId(), item.getName(), item.getGroup())
        if itemType is Grade:
            return "'{}', '{}', '{}'".format(
                item.getStudentId(),
                item.getAssignmentId(),
                item.getGrade() if item.getGrade() is not None else "NULL")
        if itemType is Assignment:
            return "'{}', '{}', '{:%d.%m.%Y}'".format(item.getAssignmentId(), item.getDescription(), item.getDeadline())

    @staticmethod
    def convertTuples(tupleList: List[Tuple], itemType: type):
        newList = []
        newItem = None
        for item in tupleList:
            if itemType is Student:
                newItem = Student(item[0], item[1], item[2])
            elif itemType is Grade:
                newItem = Grade(item[0], item[1], item[2] if item[2] != "NULL" else None)
            elif itemType is Assignment:
                newItem = Assignment(item[0], item[1], TypeParser.parseDate(item[2], InvalidAssignmentDeadline))
            newList.append(newItem)
        return newList

    @staticmethod
    def updateString(item):
        itemType: type = type(item)
        if itemType is Student:
            return "name = '{}', `group` = '{}'".format(item.getName(), item.getGroup())
        if itemType is Grade:
            return "grade = '{}'".format(item.getGrade() if item.getGrade() is not None else "NULL")
        if itemType is Assignment:
            return "description = '{}', deadline = '{:%d.%m.%Y}'".format(item.getDescription(), item.getDeadline())
