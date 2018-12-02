from repository.Repository import Repository


class FileRepository(Repository):

    def __init__(self, itemType: type, fileName: str):
        Repository.__init__(self, itemType)
        self.__fileName = fileName

    def addItem(self, item):
        self.__loadList()
        Repository.addItem(self, item)
        self.__saveList()

    def updateItem(self, item):
        self.__loadList()
        Repository.updateItem(self, item)
        self.__saveList()

    def getItems(self):
        self.__loadList()
        Repository.getItems(self)

    def getItem(self, item):
        self.__loadList()
        Repository.getItem(self, item)

    def deleteItem(self, item):
        self.__loadList()
        Repository.deleteItem(self, item)
        self.__saveList()

    def __loadList(self):
        pass

    def __saveList(self):
        pass
