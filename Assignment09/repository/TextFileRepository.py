from lib.CustomComponents import Vector
from utils.CSVConverter import CSVConverter
from repository.FileRepository import FileRepository


class TextFileRepository(FileRepository):

    def _loadList(self):
        file = None
        try:
            file = open(self._fileName, 'r')
            self._collection = Vector.fromList(
                [CSVConverter.convertCSVToItem(self._itemType, csvString.replace('\n', ''))
                 for csvString in file.readlines()], self._itemType)
        except FileNotFoundError:
            self._collection = Vector(self._itemType)
        finally:
            if file is not None:
                file.close()

    def _saveList(self):
        file = None
        try:
            file = open(self._fileName, 'w')
            file.writelines([CSVConverter.convertItemToCSV(item) + "\n"
                             for item in self._collection])
        finally:
            if file is not None:
                file.close()
