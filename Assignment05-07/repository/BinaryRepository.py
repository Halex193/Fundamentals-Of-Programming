import pickle

from repository.FileRepository import FileRepository


class BinaryRepository(FileRepository):

    def __loadList(self):
        file = None
        try:
            file = open(self.__fileName, 'rb')
            self.__collection = pickle.load(file)
        except FileNotFoundError:
            self.__collection = []
        finally:
            if file is not None:
                file.close()

    def __saveList(self):
        file = None
        try:
            file = open(self.__fileName, 'wb')
            pickle.dump(self.__collection, file)
        finally:
            if file is not None:
                file.close()
