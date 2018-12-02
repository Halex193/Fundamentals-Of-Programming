class Student:
    """
    Represents a student
    """

    def __init__(self, studentId: int, name: str = None, group: int = None):
        self.__studentId = studentId
        self.__name = name
        self.__group = group

    def getStudentId(self) -> int:
        return self.__studentId

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getGroup(self) -> int:
        return self.__group

    def setGroup(self, group: int):
        self.__group = group

    def __str__(self):
        return "{:d} - {} - {}".format(self.__studentId, self.__name, self.__group)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if self.__studentId == other.__studentId:
            return True
        return False

    def __copy__(self):
        return Student(self.__studentId, self.__name, self.__group)
