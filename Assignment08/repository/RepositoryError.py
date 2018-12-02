class RepositoryError(RuntimeError):
    pass


class DuplicateItemError(RepositoryError):
    def __init__(self, itemType):
        self.__itemType = itemType

    def getItemType(self):
        return self.__itemType


class RepositoryTypeError(Exception):
    pass

