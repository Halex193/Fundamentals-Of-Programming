from copy import copy
from typing import List


class ChangesStack:
    """
    The stack of changes committed to the repository
    """

    class Change:
        """
        Defines a change
        """

        def __init__(self, item):
            self.__item = copy(item)

        def getItem(self):
            return self.__item

    class ItemAdded(Change):
        pass

    class ItemRemoved(Change):
        pass

    def __init__(self, changesHandler):
        self.__changesStack = []
        self.__currentCommit = []
        self.__currentIndex = -1
        self.__changesHandler = changesHandler

    def beginCommit(self):
        """
        Initializes a new commit
        """
        self.__currentCommit = []

    def endCommit(self):
        """
        Appends the current commit to the changes stack
        """
        self.__changesStack = self.__changesStack[:self.__currentIndex + 1]
        self.__changesStack.append(self.__currentCommit)
        self.__currentIndex += 1

    def addChange(self, change: Change, newCommit=False):
        """
        Adds the change to the current commit
        """
        if newCommit:
            self.beginCommit()

        self.__currentCommit.append(change)

        if newCommit:
            self.endCommit()

    def undo(self) -> bool:
        """
        Undoes the last operation
        :return: True if succeeded, False otherwise
        """
        if self.__currentIndex == -1:
            return False
        commit: List[ChangesStack.Change] = self.__changesStack[self.__currentIndex]
        self.__changesHandler.handleChanges(commit, reverse=True)
        self.__currentIndex -= 1
        return True

    def redo(self) -> bool:
        """
        Reverses the last undo operation
        :return: True if succeeded, False otherwise
        """
        if self.__currentIndex == len(self.__changesStack) - 1:
            return False
        commit: List[ChangesStack.Change] = self.__changesStack[self.__currentIndex + 1]
        self.__changesHandler.handleChanges(commit, reverse=False)
        self.__currentIndex += 1
        return True

    def clearStack(self):
        """
        Clears the changes stack
        """
        self.__changesStack = []
        self.__currentCommit = []
        self.__currentIndex = -1


class ChangesHandler:
    # @abstractmethod
    def handleChanges(self, changesList: List[ChangesStack.Change], reverse: bool):
        pass
