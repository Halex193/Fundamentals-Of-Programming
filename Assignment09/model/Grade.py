class Grade:
    """
    Represents a grade
    """

    def __init__(self, studentId: int, assignmentId: int, grade: int = None):
        self.__studentId = studentId
        self.__assignmentId = assignmentId
        self.__grade = grade

    def getAssignmentId(self) -> int:
        return self.__assignmentId

    def getStudentId(self) -> int:
        return self.__studentId

    def getGrade(self) -> int:
        return self.__grade

    def setGrade(self, grade: int):
        self.__grade = grade

    def __str__(self):
        gradeText = str(self.__grade) if self.__grade is not None else "No grade"
        return "{:d} - {:d} - {}".format(self.__studentId, self.__assignmentId, gradeText)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if self.__studentId == other.__studentId and self.__assignmentId == other.__assignmentId:
            return True
        return False

    def __copy__(self):
        return Grade(self.__studentId, self.__assignmentId, self.__grade)
