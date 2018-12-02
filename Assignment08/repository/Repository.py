from copy import copy

from repository.RepositoryError import RepositoryTypeError, DuplicateItemError


class Repository:
    """
    Holds and provides access to a collection of identifiable objects
    """

    def __init__(self, itemType: type):
        self.__collection = []
        self.__itemType = itemType

    def checkType(self, item):
        if type(item) is not self.__itemType:
            raise RepositoryTypeError()

    def addItem(self, item):
        self.checkType(item)
        if item in self.__collection:
            raise DuplicateItemError(self.__itemType)
        self.__collection.append(item)

    def getItems(self):
        return [copy(item) for item in self.__collection]

    def getItem(self, item):
        self.checkType(item)
        for collectionItem in self.__collection:
            if collectionItem == item:
                return copy(collectionItem)
        return None

    def updateItem(self, item):
        for i in range(len(self.__collection)):
            if self.__collection[i] == item:
                self.__collection[i] = item

    def deleteItem(self, item):
        self.__collection.remove(item)
