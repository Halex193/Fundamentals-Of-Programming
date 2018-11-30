from model.CSVConverter import CSVConverter
from repository.FileRepository import FileRepository


class TextFileRepository(FileRepository):

    def __loadList(self):
        file = None
        try:
            file = open(self.__fileName, 'r')
            self.__collection = [CSVConverter.convertCSVToItem(self.__itemType, csvString)
                                 for csvString in file.readlines()]
        except FileNotFoundError:
            self.__collection = []
        finally:
            if file is not None:
                file.close()

    def __saveList(self):
        file = None
        try:
            file = open(self.__fileName, 'w')
            file.writelines([CSVConverter.convertItemToCSV(item)
                             for item in self.__collection])
        finally:
            if file is not None:
                file.close()
