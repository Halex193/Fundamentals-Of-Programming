from datetime import date
from typing import List, Type, Union

from logic.AssignmentController import AssignmentController
from logic.ChangesStack import ChangesStack, ChangesHandler
from logic.GradeController import GradeController
from logic.StudentController import StudentController
from model.Assignment import Assignment
from model.Grade import Grade
from model.Student import Student
from repository.RepositoryWrapper import RepositoryWrapper


class ControllerWrapper(ChangesHandler):
    def __init__(self, repositoryWrapper: RepositoryWrapper, currentDate: date):
        self.__repositoryWrapper = repositoryWrapper
        self.__changesStack = ChangesStack(self)

        studentRepository = repositoryWrapper.getRepository(Student)
        gradeRepository = repositoryWrapper.getRepository(Grade)
        assignmentRepository = repositoryWrapper.getRepository(Assignment)
        self.__studentController = StudentController(studentRepository, self)
        self.__assignmentRepository = AssignmentController(repositoryWrapper.getRepository(Assignment), self)
        self.__gradeController = GradeController(studentRepository, gradeRepository,
                                                 assignmentRepository, currentDate, self)

    def cascadeDelete(self, item):
        if type(item) is Student or Assignment:
            gradeRepository = self.__repositoryWrapper.getRepository(Grade)
            gradeList = gradeRepository.getItems()
            linkedGrades = [grade for grade in gradeList if self.__gradeLinked(grade, item)]
            for grade in linkedGrades:
                self.__changesStack.addChange(ChangesStack.ItemRemoved(grade))
                gradeRepository.deleteItem(grade)
            self.__changesStack.endCommit()

    @staticmethod
    def __gradeLinked(grade: Grade, item):
        if type(item) is Student:
            return grade.getStudentId() == item.getStudentId()
        elif type(item) is Assignment:
            return grade.getAssignmentId() == item.getAssignmentId()

    def populateRepository(self):
        """
        Adds default data to the repository
        """
        self.__studentController.addRandomStudents(50)
        self.__assignmentRepository.addRandomAssignments(50)
        self.__gradeController.addRandomGrades(40, 40, 50)

        self.clearHistory()

    def handleChanges(self, changesList: List[ChangesStack.Change], reverse):
        """
        Handles changes provided by the ChangesStack
        """
        if reverse:
            functionDict = {
                ChangesStack.ItemAdded: self.removeItem,
                ChangesStack.ItemRemoved: self.addItem
            }
            iteratedList = reversed(changesList)
        else:
            functionDict = {
                ChangesStack.ItemAdded: self.addItem,
                ChangesStack.ItemRemoved: self.removeItem
            }
            iteratedList = changesList

        for change in iteratedList:
            itemType: Type[Union[ChangesStack.ItemAdded, ChangesStack.ItemRemoved]] = type(change)
            item = change.getItem()
            functionDict[itemType](item)

    def addItem(self, item):
        self.__repositoryWrapper.getRepository(type(item)).addItem(item)

    def removeItem(self, item):
        self.__repositoryWrapper.getRepository(type(item)).deleteItem(item)

    def clearHistory(self):
        self.__changesStack.clearStack()

    def undo(self):
        """
        Undoes the last operation
        """
        return self.__changesStack.undo()

    def redo(self):
        """
        Reverses the last undo operation
        """
        return self.__changesStack.redo()
