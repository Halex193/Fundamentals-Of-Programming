class RepositoryError(RuntimeError):
    pass


class DuplicateItemError(RepositoryError):
    def __init__(self, itemType):
        self.__itemType = itemType

    def getItemType(self):
        return self.__itemType


class RepositoryTypeError(RepositoryError):
    pass


class ItemNotFoundError(RepositoryError):
    pass
