from logic.ChangesStack import ChangesStack, ChangesHandler
from model.Assignment import Assignment
from model.Student import Student
from repository.RepositoryWrapper import RepositoryWrapper

# TODO check integrity
class ControllerWrapper(ChangesHandler):
    def __init__(self, repositoryWrapper: RepositoryWrapper):
        self.__repositoryWrapper = repositoryWrapper
        self.__changesStack = ChangesStack(self)

    @staticmethod
    def parseInt(string: str, errorType: type) -> int:
        """
        Parses a number to an integer. If the conversion fails, raises the specified exception
        """
        try:
            return int(string)
        except ValueError:
            raise errorType()

    def itemAdded(self, item):
        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemAdded(item))
        self.__changesStack.endCommit()

    def itemRemoved(self, item):
        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(item))
        if type(item) is Student or Assignment:
            # gradeList = self.__grades.getStudentGrades(student)
            # for grade in gradeList:
            #     self.__changesStack.addChange(ChangesStack.ItemRemoved(grade))
            #     del self.__grades[grade]
            # TODO cascade delete
            pass
        self.__changesStack.endCommit()
