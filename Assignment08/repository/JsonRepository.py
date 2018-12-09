from repository.FileRepository import FileRepository
from utils.JSONConverter import JSONConverter


class JsonRepository(FileRepository):
    def _loadList(self):
        file = None
        try:
            file = open(self._fileName, 'r')
            self._collection = JSONConverter.convertJSONToList(self._itemType, file.read())
        except FileNotFoundError:
            self._collection = []
        finally:
            if file is not None:
                file.close()

    def _saveList(self):
        file = None
        try:
            file = open(self._fileName, 'w')
            file.write(JSONConverter.convertListToJSON(self._itemType, self._collection))
        finally:
            if file is not None:
                file.close()
