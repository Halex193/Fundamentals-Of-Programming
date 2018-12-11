import pickle

from lib.CustomComponents import Vector
from repository.FileRepository import FileRepository


class BinaryRepository(FileRepository):

    def _loadList(self):
        file = None
        try:
            file = open(self._fileName, 'rb')
            self._collection = pickle.load(file)
        except FileNotFoundError:
            self._collection = Vector(self._itemType)
        finally:
            if file is not None:
                file.close()

    def _saveList(self):
        file = None
        try:
            file = open(self._fileName, 'wb')
            pickle.dump(self._collection, file)
        finally:
            if file is not None:
                file.close()
