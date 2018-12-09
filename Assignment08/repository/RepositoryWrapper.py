from typing import Type, Union

from model.Student import Student
from model.Grade import Grade
from model.Assignment import Assignment
from repository.BinaryRepository import BinaryRepository
from repository.Repository import Repository
from repository.TextFileRepository import TextFileRepository
from repository.JsonRepository import JsonRepository


class RepositoryWrapper:
    """
    Holds all the program data
    """

    def __init__(self, storageType: str, studentsFile: str, gradesFile: str, assignmentsFile: str):
        if storageType == 'memory':
            self.__studentRepository = Repository(Student)
            self.__gradeRepository = Repository(Grade)
            self.__assignmentRepository = Repository(Assignment)
        elif storageType == 'text':
            self.__studentRepository = TextFileRepository(Student, studentsFile)
            self.__gradeRepository = TextFileRepository(Grade, gradesFile)
            self.__assignmentRepository = TextFileRepository(Assignment, assignmentsFile)
        elif storageType == 'binary':
            self.__studentRepository = BinaryRepository(Student, studentsFile)
            self.__gradeRepository = BinaryRepository(Grade, gradesFile)
            self.__assignmentRepository = BinaryRepository(Assignment, assignmentsFile)
        elif storageType == 'json':
            self.__studentRepository = JsonRepository(Student, studentsFile)
            self.__gradeRepository = JsonRepository(Grade, gradesFile)
            self.__assignmentRepository = JsonRepository(Assignment, assignmentsFile)
        elif storageType == 'sql':
            pass

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
