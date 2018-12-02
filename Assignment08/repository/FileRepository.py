from repository.Repository import Repository


class FileRepository(Repository):

    def __init__(self, itemType: type, fileName: str):
        Repository.__init__(self, itemType)
        self._fileName = fileName

    def addItem(self, item):
        self._loadList()
        Repository.addItem(self, item)
        self._saveList()

    def updateItem(self, item):
        self._loadList()
        Repository.updateItem(self, item)
        self._saveList()

    def getItems(self):
        self._loadList()
        return Repository.getItems(self)

    def getItem(self, item):
        self._loadList()
        return Repository.getItem(self, item)

    def deleteItem(self, item):
        self._loadList()
        Repository.deleteItem(self, item)
        self._saveList()

    def _loadList(self):
        raise NotImplementedError

    def _saveList(self):
        raise NotImplementedError