from repository.Repository import Repository


class FileRepository(Repository):

    def addItem(self, item):
        self.__getList()
        Repository.addItem(self, item)
        self.__updateList()

    def updateItem(self, item):
        self.__getList()
        Repository.updateItem(self, item)
        self.__updateList()

    def getItems(self):
        self.__getList()
        Repository.getItems(self)

    def getItem(self, item):
        self.__getList()
        Repository.getItem(self, item)

    def deleteItem(self, item):
        self.__getList()
        Repository.deleteItem(self, item)
        self.__updateList()

    def __getList(self):
        pass

    def __updateList(self):
        pass
