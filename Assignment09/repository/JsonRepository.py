from lib.CustomComponents import Vector
from repository.FileRepository import FileRepository
from utils.JSONConverter import JSONConverter


class JsonRepository(FileRepository):
    def _loadList(self):
        file = None
        try:
            file = open(self._fileName, 'r')
            self._collection = Vector.fromList(JSONConverter.convertJSONToList(
                self._itemType,
                file.read()
            ), self._itemType)
        except FileNotFoundError:
            self._collection = Vector(self._itemType)
        finally:
            if file is not None:
                file.close()

    def _saveList(self):
        file = None
        try:
            file = open(self._fileName, 'w')
            file.write(JSONConverter.convertListToJSON(self._itemType, Vector.toList(self._collection)))
        finally:
            if file is not None:
                file.close()
