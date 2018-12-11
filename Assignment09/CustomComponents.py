from typing import List
from unittest import TestCase


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
            raise IndexError
        return self.__items[key]

    def __setitem__(self, key, item):
        if type(key) is not int:
            raise TypeError
        if key < 0 or key >= self.__len:
            raise IndexError
        if type(item) is not self.__itemType:
            raise TypeError

        self.__items[key] = item

    def __delitem__(self, key):
        if type(key) is not int:
            raise TypeError
        if key < 0 or key >= self.__len:
            raise IndexError

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
        self.__items.append(item)
        self.__len += 1

    def __iter__(self):
        self.__pointer = 0
        return self

    def __next__(self):
        if self.__pointer == self.__len:
            raise StopIteration
        return self.__items[self.__pointer]


def sortList(list: List, compare: callable) -> List:
    """
    Sorts the list by the criteria imposed by the compare function
    :param list: A list of elements - will be modified
    :param compare: A function that compares two elements and returns the result accordingly:
    1 -> The first item is greater than the second one
    0 -> The items are equal
    -1 -> The second item is greater than the first one
    :return: The sorted list
    """
    length = len(list)
    gap = length // 2

    while gap > 0:

        for i in range(gap, length):

            comparedElement = list[i]

            j = i
            while j >= gap and compare(list[j - gap], comparedElement) == 1:
                list[j] = list[j - gap]
                j -= gap
            list[j] = comparedElement
        gap //= 2

    return list


def filterList(list: List, accepted: callable) -> List:
    """
    Filters the list according to the acceptance function provided
    :param list: A list of elements - will be modified
    :param accepted: A function that establishes if an element should be kept in the list or not
    :return: The filtered list
    """
    i = 0
    while i < len(list):
        if accepted(list[i]):
            i += 1
        else:
            del list[i]
    return list


class TestComponents(TestCase):

    def setUp(self):
        self.integerVector: Vector = Vector(int)
        self.stringVector: Vector = Vector(str)
        self.tupleVector: Vector = Vector(tuple)

    def tearDown(self):
        self.integerVector = None
        self.stringVector = None
        self.tupleVector = None

    def testCreate(self):
        self.assertEqual(len(self.integerVector), 0)
        self.assertEqual(len(self.stringVector), 0)
        self.assertEqual(len(self.tupleVector), 0)

    def testAdd(self):
        with self.assertRaises(TypeError):
            self.integerVector.addItem("item")
        with self.assertRaises(TypeError):
            self.stringVector.addItem((1, 3))
        with self.assertRaises(TypeError):
            self.tupleVector.addItem("item")

        self.integerVector.addItem(1)
        self.assertEqual(len(self.integerVector), 1)
        self.integerVector.addItem(2)
        self.assertEqual(len(self.integerVector), 2)

    def testRead(self):
        self.integerVector.addItem(1)
        self.assertEqual(self.integerVector[0], 1)
        self.integerVector.addItem(2)
        self.assertEqual(self.integerVector[0], 1)
        self.assertEqual(self.integerVector[1], 2)
        with self.assertRaises(IndexError):
            unused = self.integerVector[-1]
        with self.assertRaises(IndexError):
            unused = self.integerVector[2]

        self.stringVector.addItem("1")
        self.assertEqual(self.stringVector[0], "1")
        self.stringVector.addItem("2")
        self.assertEqual(self.stringVector[0], "1")
        self.assertEqual(self.stringVector[1], "2")
        with self.assertRaises(IndexError):
            unused = self.stringVector[-1]
        with self.assertRaises(IndexError):
            unused = self.stringVector[2]

        self.tupleVector.addItem((1, 1))
        self.assertEqual(self.tupleVector[0], (1, 1))
        self.tupleVector.addItem((2, 2))
        self.assertEqual(self.tupleVector[0], (1, 1))
        self.assertEqual(self.tupleVector[1], (2, 2))
        with self.assertRaises(IndexError):
            unused = self.tupleVector[-1]
        with self.assertRaises(IndexError):
            unused = self.tupleVector[2]

    def testUpdate(self):
        self.integerVector.addItem(1)
        self.integerVector.addItem(2)
        self.integerVector.addItem(3)
        self.integerVector[0] = 4
        self.assertEqual(len(self.integerVector), 3)
        self.assertEqual(self.integerVector[0], 4)
        self.assertEqual(self.integerVector[1], 2)
        self.assertEqual(self.integerVector[2], 3)

    def testDelete(self):
        self.integerVector.addItem(1)
        self.integerVector.addItem(2)
        self.integerVector.addItem(3)
        del self.integerVector[0]
        self.assertEqual(len(self.integerVector), 2)
        self.assertEqual(self.integerVector[0], 2)
        self.assertEqual(self.integerVector[1], 3)

    def testSort(self):
        integerList = [5, 4, 3, 2, 1]

        def compareFunction(a, b):
            return (a - b) / abs(a - b)

        self.assertEqual(sortList(integerList, compareFunction), [1, 2, 3, 4, 5])

    def testFilter(self):
        integerList = [5, 4, 3, 2, 1]

        def acceptanceFunction(a):
            return a % 2 == 0

        self.assertEqual(filterList(integerList, acceptanceFunction), [4, 2])
