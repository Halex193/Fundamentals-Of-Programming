from copy import copy

from repository.RepositoryError import *


class Repository:
    """
    Holds and provides access to a collection of identifiable objects
    """

    def __init__(self, itemType: type):
        self._collection = []
        self._itemType = itemType

    def checkType(self, item):
        if type(item) is not self._itemType:
            raise RepositoryTypeError()

    def addItem(self, item):
        self.checkType(item)
        if item in self._collection:
            raise DuplicateItemError(self._itemType)
        self._collection.append(item)

    def getItems(self):
        if len(self._collection) == 0:
            return []
        return [copy(item) for item in self._collection]

    def getItem(self, item):
        self.checkType(item)
        for collectionItem in self._collection:
            if collectionItem == item:
                return copy(collectionItem)
        return None

    def updateItem(self, item):
        for i in range(len(self._collection)):
            if self._collection[i] == item:
                self._collection[i] = item
                return
        raise ItemNotFoundError

    def deleteItem(self, item):
        try:
            self._collection.remove(item)
        except ValueError:
            raise ItemNotFoundError
