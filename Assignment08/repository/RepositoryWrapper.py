from typing import Type, Union

from model.Student import Student
from model.Grade import Grade
from model.Assignment import Assignment
from repository.BinaryRepository import BinaryRepository
from repository.MySQLRepository import MySQLRepository
from repository.Repository import Repository
from repository.TextFileRepository import TextFileRepository
from repository.JsonRepository import JsonRepository
from utils.MySQLConnector import MySQLConnector


class RepositoryWrapper:
    """
    Holds all the program data
    """

    def __init__(
            self, storageType: str,
            studentRepositoryLocation: str,
            gradeRepositoryLocation: str,
            assignmentRepositoryLocation: str
    ):
        if storageType == 'memory':
            self.__studentRepository = Repository(Student)
            self.__gradeRepository = Repository(Grade)
            self.__assignmentRepository = Repository(Assignment)
        elif storageType == 'text':
            self.__studentRepository = TextFileRepository(Student, studentRepositoryLocation)
            self.__gradeRepository = TextFileRepository(Grade, gradeRepositoryLocation)
            self.__assignmentRepository = TextFileRepository(Assignment, assignmentRepositoryLocation)
        elif storageType == 'binary':
            self.__studentRepository = BinaryRepository(Student, studentRepositoryLocation)
            self.__gradeRepository = BinaryRepository(Grade, gradeRepositoryLocation)
            self.__assignmentRepository = BinaryRepository(Assignment, assignmentRepositoryLocation)
        elif storageType == 'json':
            self.__studentRepository = JsonRepository(Student, studentRepositoryLocation)
            self.__gradeRepository = JsonRepository(Grade, gradeRepositoryLocation)
            self.__assignmentRepository = JsonRepository(Assignment, assignmentRepositoryLocation)
        elif storageType == 'sql':
            connection = MySQLConnector().getConnection()

            self.__studentRepository = MySQLRepository(Student, studentRepositoryLocation, connection)
            self.__gradeRepository = MySQLRepository(Grade, gradeRepositoryLocation, connection)
            self.__assignmentRepository = MySQLRepository(Assignment, assignmentRepositoryLocation, connection)

        self.__repositories = {
            Student: self.__studentRepository,
            Grade: self.__gradeRepository,
            Assignment: self.__assignmentRepository
        }

    def getRepository(self, repositoryType: Type[Union[Student, Grade, Assignment]]) -> Repository:
        """
        Returns the Repository for the given item type
        """
        return self.__repositories[repositoryType]

    def isEmpty(self) -> bool:
        if len(self.__studentRepository.getItems()) != 0:
            return False
        if len(self.__gradeRepository.getItems()) != 0:
            return False
        if len(self.__assignmentRepository.getItems()) != 0:
            return False

        return True
