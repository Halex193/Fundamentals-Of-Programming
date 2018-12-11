from mysql.connector import MySQLConnection
from repository.Repository import Repository
from repository.RepositoryError import DuplicateItemError, ItemNotFoundError
from utils.MySQLConnector import MySQLConnector


class MySQLRepository(Repository):
    """
    Repository backed up by a database table
    """

    def __init__(self, itemType: type, tableName: str, connection: MySQLConnection):
        Repository.__init__(self, itemType)
        self.__tableName = tableName
        self.__connection = connection
        self.__cursor = connection.cursor(buffered=True)

    def addItem(self, item):
        self.checkType(item)
        self.__cursor.execute("SELECT * FROM " + self.__tableName + " WHERE " + MySQLConnector.idCheckString(item))
        if self.__cursor.rowcount > 0:
            raise DuplicateItemError(self._itemType)
        self.__cursor.execute("INSERT INTO " + self.__tableName + " VALUES (" + MySQLConnector.valuesString(item) + ")")
        self.__connection.commit()

    def getItems(self):
        self.__cursor.execute("SELECT * FROM " + self.__tableName)
        return MySQLConnector.convertTuples(self.__cursor.fetchall(), self._itemType)

    def getItem(self, item):
        self.checkType(item)
        self.__cursor.execute("SELECT * FROM " + self.__tableName + " WHERE " + MySQLConnector.idCheckString(item))
        if self.__cursor.rowcount > 0:
            return MySQLConnector.convertTuples([self.__cursor.fetchone()], self._itemType)[0]
        return None

    def updateItem(self, item):
        self.__cursor.execute("SELECT * FROM " + self.__tableName + " WHERE " + MySQLConnector.idCheckString(item))
        if self.__cursor.rowcount > 0:
            self.__cursor.execute("UPDATE " + self.__tableName + " SET " +
                                  MySQLConnector.updateString(item) + " WHERE " + MySQLConnector.idCheckString(item))
            self.__connection.commit()
            return
        raise ItemNotFoundError

    def deleteItem(self, item):
        self.__cursor.execute("SELECT * FROM " + self.__tableName + " WHERE " + MySQLConnector.idCheckString(item))
        if self.__cursor.rowcount > 0:
            self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + MySQLConnector.idCheckString(item))
            self.__connection.commit()
            return
        raise ItemNotFoundError
