from typing import Type, Union

from model.Student import Student
from model.Grade import Grade
from model.Assignment import Assignment
from repository.Repository import Repository


class RepositoryError(RuntimeError):
    pass


class DuplicateItemError(RepositoryError):
    pass


class RepositoryTypeError(RepositoryError):
    pass


class RepositoryWrapper:
    """
    Holds all the program data
    """

    def __init__(self):
        self.__studentRepository = Repository(Student)
        self.__gradeRepository = Repository(Grade)
        self.__assignmentRepository = Repository(Assignment)

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
