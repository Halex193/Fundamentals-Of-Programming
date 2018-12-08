from typing import List


class Vector:
    """
    Custom vector class
    """

    def __init__(self, itemType: type):
        self.__items = []
        self.__len = 0
        self.__itemType = itemType
        self.__pointer = 0

    def __len__(self):
        return self.__len

    def __getitem__(self, key):
        if type(key) is not int:
            raise TypeError
        if key < 0 or key >= self.__len:
            raise ValueError
        return self.__items[key]

    def __setitem__(self, key, item):
        if type(key) is not int:
            raise TypeError
        if key < 0 or key >= self.__len:
            raise ValueError
        if type(item) is not self.__itemType:
            raise TypeError

        self.__items[key] = item

    def __delitem__(self, key):
        if type(key) is not int:
            raise TypeError
        if key < 0 or key >= self.__len:
            raise ValueError

        del self.__items[key]
        self.__len -= 1

    def addItem(self, item):
        """
        Adds an item to the vector
        :param item: Must be of the specified type
        :raises: TypeError if the item is not of the specified type
        """
        if type(item) is not self.__itemType:
            raise TypeError
        self.__items[self.__len] = item
        self.__len += 1

    def __iter__(self):
        self.__pointer = 0
        return self

    def __next__(self):
        if self.__pointer == self.__len:
            raise StopIteration
        return self.__items[self.__pointer]


def sortList(initialList: List, compare: callable) -> List:
    """
    Sorts the list by the criteria imposed by the compare function
    :param initialList: A list of elements - will be modified
    :param compare: A function that compares two elements and returns the result accordingly:
    1 -> The first item is greater than the second one
    0 -> The items are equal
    -1 -> The second item is greater than the first one
    :return: The sorted list
    """
    pass


def filterList(initialList: List, accepted: callable) -> List:
    """
    Filters the list according to the acceptance function provided
    :param initialList: A list of elements - will be modified
    :param accepted: A function that establishes if an element should be kept in the list or not
    :return: The filtered list
    """
    pass
