from datetime import date


class Assignment:
    """
    Represents an assignment
    """

    def __init__(self, assignmentId: int, description: str = None, deadline: date = None):
        self.__assignmentId = assignmentId
        self.__description = description
        self.__deadline = deadline

    def getAssignmentId(self):
        return self.__assignmentId

    def getDescription(self):
        return self.__description

    def setDescription(self, description: str):
        self.__description = description

    def getDeadline(self):
        return self.__deadline

    def setDeadline(self, deadline: date):
        self.__deadline = deadline

    def __str__(self):
        return str(self.__assignmentId) + " - " + self.__description + " - " + str(self.__deadline)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if self.__assignmentId == other.__assignmentId:
            return True
        return False

    def __copy__(self):
        return Assignment(self.__assignmentId, self.__description, self.__deadline)
