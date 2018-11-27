"""
This is the logic module
"""
import datetime
import random
from copy import copy
from typing import Type, Union

from repository import *
from validation import *


class ChangesStack:
    """
    The stack of changes committed to the repository
    """

    class Change:
        """
        Defines a change
        """

        def __init__(self, item):
            self.__item = copy(item)

        def getItem(self):
            return self.__item

    class ItemAdded(Change):
        pass

    class ItemRemoved(Change):
        pass

    def __init__(self, changesHandler):
        self.__changesStack = []
        self.__currentCommit = []
        self.__currentIndex = -1
        self.__changesHandler = changesHandler

    def beginCommit(self):
        """
        Initializes a new commit
        """
        self.__currentCommit = []

    def endCommit(self):
        """
        Appends the current commit to the chages stack
        """
        self.__changesStack = self.__changesStack[:self.__currentIndex + 1]
        self.__changesStack.append(self.__currentCommit)
        self.__currentIndex += 1

    def addChange(self, change: Change):
        """
        Adds the change to the current commit
        """
        self.__currentCommit.append(change)

    def undo(self) -> bool:
        """
        Undoes the last operation
        :return: True if succeeded, False otherwise
        """
        if self.__currentIndex == -1:
            return False
        commit: List[ChangesStack.Change] = self.__changesStack[self.__currentIndex]
        self.__changesHandler.handleChanges(commit, reverse=True)
        self.__currentIndex -= 1
        return True

    def redo(self) -> bool:
        """
        Reverses the last undo operation
        :return: True if succeeded, False otherwise
        """
        if self.__currentIndex == len(self.__changesStack) - 1:
            return False
        commit: List[ChangesStack.Change] = self.__changesStack[self.__currentIndex + 1]
        self.__changesHandler.handleChanges(commit, reverse=False)
        self.__currentIndex += 1
        return True

    def clearStack(self):
        """
        Clears the changes stack
        """
        self.__changesStack = []
        self.__currentCommit = []
        self.__currentIndex = -1


class ChangesHandler:
    # @abstractmethod
    def handleChanges(self, changesList: List[ChangesStack.Change], reverse: bool):
        pass


class DuplicateAssignment(CustomError):
    pass


class LogicComponent(ChangesHandler):
    """
    Provides all the logic functions of the software
    """

    def __init__(self, repository: Repository, currentDate: date):
        self.__repository = repository
        self.__students: StudentCollection = repository.getStudents()
        self.__grades: GradeCollection = repository.getGrades()
        self.__assignments: AssignmentCollection = repository.getAssignments()
        self.__changesStack: ChangesStack = ChangesStack(self)
        self.currentDate = currentDate

    def handleChanges(self, changesList: List[ChangesStack.Change], reverse):
        """
        Handles changes provided by the ChangesStack
        """
        if reverse:
            functionDict = {
                ChangesStack.ItemAdded: self.removeItem,
                ChangesStack.ItemRemoved: self.addItem
            }
            for change in reversed(changesList):
                itemType: Type[Union[ChangesStack.ItemAdded, ChangesStack.ItemRemoved]] = type(change)
                item = change.getItem()
                functionDict[itemType](item)
        else:
            functionDict = {
                ChangesStack.ItemAdded: self.addItem,
                ChangesStack.ItemRemoved: self.removeItem
            }
            for change in changesList:
                itemType = type(change)
                item = change.getItem()
                functionDict[itemType](item)

    def addItem(self, item):
        itemType = type(item)
        if itemType is Student:
            self.__students.addStudent(item)
        elif itemType is Grade:
            self.__grades.addGrade(item)
        elif itemType is Assignment:
            self.__assignments.addAssignment(item)

    def removeItem(self, item):
        itemType = type(item)
        if itemType is Student:
            del self.__students[item]
        elif itemType is Grade:
            del self.__grades[item]
        elif itemType is Assignment:
            del self.__assignments[item]

    def populateRepository(self):
        """
        Adds default data to the repository
        """
        self.addRandomStudents(50)
        self.addRandomAssignments(50)
        self.addRandomGrades(40, 40, 50)

        self.clearHistory()

    def addRandomStudents(self, number):
        firstNames = [
            "Richard",
            "Andrew",
            "John",
            "Ray",
            "Ana",
            "Jessica",
            "Bob",
            "Tyler",
            "Lawrence",
            "Kimberly",
            "Scarlet",
            "Diana",
            "Sherlock",
            "Damien",
            "Kathy"
        ]
        lastNames = [
            "Brossard",
            "Crosland",
            "Hutton",
            "Holmes",
            "Hudson",
            "Watson",
            "Heaton",
            "Nelligan",
            "Spears",
            "Redman",
            "Zion",
            "Lambert"
        ]
        groups = [
            911,
            912,
            913,
            914,
            915,
            916,
            917
        ]
        for i in range(number):
            firstName = random.choice(firstNames)
            lastName = random.choice(lastNames)
            group = random.choice(groups)
            self.addStudent(firstName + " " + lastName, group)

    def addRandomAssignments(self, number):
        descriptionTitles = [
            "project",
            "documentary",
            "study",
        ]
        descriptionSubjects = [
            "importance",
            "problem",
            "execution",
            "reuse",
            "toxicity",
            "revolution",
            "discovery",
            "superiority",
            "union",
            "replication"
        ]
        descriptionAdjectives = [
            "dumb",
            "dark",
            "unused",
            "unseen",
            "reheated",
            "purple",
            "the chosen",
            "fast",
            "stupid",
            "left-handed",
            "drunk",
            "smart-ass"
        ]
        descriptionNouns = [
            "programmers",
            "memes",
            "weed",
            "meals",
            "chemistry",
            "doors",
            "birds",
            "cars",
            "PCs",
            "floppy disks",
            "refrigerators",
            "ice",
            "mountain trip",
            "stone age",
            "underground cavern",
            "board games",
            "drawings"
        ]

        for i in range(number):
            descriptionTitle = random.choice(descriptionTitles)
            descriptionSubject = random.choice(descriptionSubjects)
            descriptionAdjective = random.choice(descriptionAdjectives)
            descriptionNoun = random.choice(descriptionNouns)
            description = "A " + descriptionTitle + " about the " + descriptionSubject + " of " + descriptionAdjective + \
                          " " + descriptionNoun

            assignmentDate = LogicComponent.randomDate(date(2018, 1, 1), date(2020, 1, 1))
            dateString = str(assignmentDate.day) + "." + str(assignmentDate.month) + "." + str(assignmentDate.year)
            self.addAssignment(description, dateString)

    @staticmethod
    def randomDate(start, end):
        """
        Generate a random datetime between `start` and `end`
        """
        return start + datetime.timedelta(
            # Get a random amount of seconds between `start` and `end`
            seconds=random.randint(0, int((end - start).total_seconds())),
        )

    def addRandomGrades(self, studentNumber, assignmentNumber, number):
        for i in range(number):
            studentId = random.randint(0, studentNumber - 1)
            assignmentId = random.randint(0, assignmentNumber - 1)
            grade = random.randint(0, 10)
            if grade == 0:
                grade = None
            self.__grades.addGrade(Grade(studentId, assignmentId, grade))

    # Manage Students menu

    def listStudents(self) -> List[Student]:
        """
        Returns a list of students sorted in ascending order by their IDs
        """
        return sorted([student for student in self.__students], key=lambda student: student.getStudentId())

    def addStudent(self, name: str, group: str) -> Student:
        """
        Adds a student to the repository
        """
        group = self.parseInt(group, InvalidStudentGroup)
        student = Student(0, name, group)
        ValidationUtils.Student.validateStudent(student)

        newStudent = self.__students.addStudent(student)

        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemAdded(newStudent))
        self.__changesStack.endCommit()

        return newStudent

    @staticmethod
    def parseInt(string: str, errorType: type) -> int:
        """
        Parses a number to an integer. If the conversion fails, raises the specified exception
        """
        try:
            return int(string)
        except ValueError:
            raise errorType()

    def removeStudent(self, studentId: str):
        """
        Removes a student from the repository
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        student = self.findStudent(studentId)
        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(student))

        del self.__students[student]
        gradeList = self.__grades.getStudentGrades(student)
        for grade in gradeList:
            self.__changesStack.addChange(ChangesStack.ItemRemoved(grade))
            del self.__grades[grade]
        self.__changesStack.endCommit()

    def findStudent(self, studentId) -> Student:
        """
        Searches a student and returns it if found. Raises InvalidStudentId if not
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        if studentId not in [student.getStudentId() for student in self.__students]:
            raise InvalidStudentId
        else:
            return self.__students[studentId]

    def updateStudent(self, studentId, name: str, group: str):
        """
        Updates the student data
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        group = self.parseInt(group, InvalidStudentGroup)
        ValidationUtils.Student.validateStudent(Student(0, name, group))
        student = self.findStudent(studentId)
        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(student))
        student.setName(name)
        student.setGroup(group)
        self.__changesStack.addChange(ChangesStack.ItemAdded(student))
        self.__changesStack.endCommit()

    # Manage Assignments Menu

    def listAssignments(self) -> List[Assignment]:
        """
        Returns a list of assignments sorted in ascending order by their IDs
        """
        return sorted([assignment for assignment in self.__assignments],
                      key=lambda assignment: assignment.getAssignmentId())

    def addAssignment(self, description: str, deadline: str) -> Assignment:
        """
        Adds a assignment to the repository
        """
        deadline = self.parseDate(deadline, InvalidAssignmentDeadline)
        assignment = Assignment(0, description, deadline)
        ValidationUtils.Assignment.validateAssignment(assignment)

        newAssignment = self.__assignments.addAssignment(assignment)

        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemAdded(newAssignment))
        self.__changesStack.endCommit()

        return newAssignment

    @staticmethod
    def parseDate(string: str, errorType: type) -> date:
        """
        Parses a string to a date. Valid format: day.month.year .
        If the conversion fails, raises the specified exception
        """
        try:
            symbols = string.split('.')
            if len(symbols) != 3:
                raise errorType()
            day = int(symbols[0])
            month = int(symbols[1])
            year = int(symbols[2])
            return date(year, month, day)
        except ValueError:
            raise errorType()

    def removeAssignment(self, assignmentId: str):
        """
        Removes an assignment from the repository
        """
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.findAssignment(assignmentId)
        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(assignment))
        del self.__assignments[assignment]
        gradeList = self.__grades.getAssignmentGrades(assignment)
        for grade in gradeList:
            self.__changesStack.addChange(ChangesStack.ItemRemoved(grade))
            del self.__grades[grade]
        self.__changesStack.endCommit()

    def findAssignment(self, assignmentId) -> Assignment:
        """
        Searches an assignment and returns it if found. Raises InvalidAssignmentId otherwise
        """
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        if assignmentId not in [assignment.getAssignmentId() for assignment in self.__assignments]:
            raise InvalidAssignmentId
        else:
            return self.__assignments[assignmentId]

    def updateAssignment(self, assignmentId, description: str, deadline: str):
        """
        Updates the assignment data
        """
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        deadline = self.parseDate(deadline, InvalidAssignmentDeadline)
        ValidationUtils.Assignment.validateAssignment(Assignment(0, description, deadline))
        assignment = self.findAssignment(assignmentId)
        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(assignment))
        assignment.setDescription(description)
        assignment.setDeadline(deadline)
        self.__changesStack.addChange(ChangesStack.ItemAdded(assignment))
        self.__changesStack.endCommit()

    # Give assignments menu

    def assignToStudent(self, studentId, assignmentId, newCommit=True) -> Grade:
        """
        Gives an assignment to a student
        """
        student = self.findStudent(studentId)
        assignment = self.findAssignment(assignmentId)
        try:
            newGrade = self.__grades.assign(student, assignment)
        except KeyError:
            raise DuplicateAssignment
        if newGrade is not None:
            if newCommit:
                self.__changesStack.beginCommit()
            self.__changesStack.addChange(ChangesStack.ItemAdded(newGrade))
            if newCommit:
                self.__changesStack.endCommit()
            return newGrade

    def checkGroupExistence(self, group: str):
        """
        Checks if there are any students within the specified group
        """
        group = self.parseInt(group, InvalidStudentGroup)
        if group not in [student.getGroup() for student in self.__students]:
            raise InvalidStudentGroup

    def assignToGroup(self, group: str, assignmentId: str):
        """
        Gives an assignment to the specified group
        """
        group = self.parseInt(group, InvalidStudentGroup)
        groupStudents = [student for student in self.__students if student.getGroup() == group]
        self.__changesStack.beginCommit()
        for student in groupStudents:
            try:
                self.assignToStudent(student.getStudentId(), assignmentId, newCommit=False)
            except DuplicateAssignment:
                pass
        self.__changesStack.endCommit()

    def listStudentGrades(self, studentId) -> List[Grade]:
        """
        Lists all the grades for the student with the given ID
        """
        student = self.findStudent(studentId)
        return self.__grades.getStudentGrades(student)

    def listAssignmentGrades(self, assignmentId) -> List[Grade]:
        """
        Lists all the grades for the assignment with the given ID
        """
        assignment = self.findAssignment(assignmentId)
        return self.__grades.getAssignmentGrades(assignment)

    def grade(self, studentId: str, assignmentId: str, grade: str):
        """
        Grades the student at the given assignment
        :param studentId: The ID of the student
        :param assignmentId: The ID of the assignment
        :param grade: THe grade of the assignment, an integer between 1 and 10
        :raises InvalidGrade: If an invalid grade is given
        :raises InvalidAssignmentId: If the student has not been given the assignment
        """
        self.findStudent(studentId)
        self.findAssignment(assignmentId)
        grade = self.parseInt(grade, InvalidGrade)
        if grade < 1 or grade > 10:
            raise InvalidGrade
        gradeObject = self.findGrade(studentId, assignmentId)
        if gradeObject is None or gradeObject.getGrade() is not None:
            raise InvalidAssignmentId
        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(gradeObject))
        gradeObject.setGrade(grade)
        self.__changesStack.addChange(ChangesStack.ItemAdded(gradeObject))
        self.__changesStack.endCommit()

    def getStudentUngradedAssignments(self, studentId) -> List[Assignment]:
        """
        Lists the ungraded assignments for the student with the given ID
        """
        student = self.findStudent(studentId)
        studentGrades = self.__grades.getStudentGrades(student)
        studentNoneGrades = [grade for grade in studentGrades if grade.getGrade() is None]
        return [self.findAssignment(grade.getAssignmentId()) for grade in studentNoneGrades]

    def assignmentGradable(self, studentId: str, assignmentId: str):
        """
        Checks if the assignment for a student is gradable
        :raises InvalidAssignmentId: If the assignment is not gradable
        """
        gradeObject = self.findGrade(studentId, assignmentId)
        if gradeObject is None or gradeObject.getGrade() is not None:
            raise InvalidAssignmentId

    def findGrade(self, studentId: str, assignmentId: str) -> Grade:
        """
        Finds and returns the grade of a student for a given assignment
        """
        studentId = self.parseInt(studentId, InvalidStudentId)
        assignmentId = self.parseInt(assignmentId, InvalidAssignmentId)
        return self.__grades[studentId, assignmentId]

    def getStudentsForAssignmentSortedAlphabetically(self, assignmentId) -> List[Student]:
        """
        Returns a list of all students who received a given assignment, ordered alphabetically
        """
        grades = self.listAssignmentGrades(assignmentId)
        students = [self.findStudent(grade.getStudentId()) for grade in grades]
        return sorted(students, key=lambda student: student.getName())

    def getStudentsForAssignmentSortedByGrade(self, assignmentId) -> List[Student]:
        """
        Returns a list of all students who received a given assignment, ordered by the grade for that assignment
        """
        grades = self.listAssignmentGrades(assignmentId)
        noneGrades = [grade for grade in grades if grade.getGrade() is None]
        givenGrades = [grade for grade in grades if grade.getGrade() is not None]
        sortedGrades = sorted(givenGrades, key=lambda grade: grade.getGrade(), reverse=True)
        students = [self.findStudent(grade.getStudentId()) for grade in sortedGrades + noneGrades]
        return students

    def getStudentsSortedByAverage(self) -> List[Tuple[Student, float]]:
        """
        Returns a list of tuples with the students and their average grades,
        sorted in descending order of the average grade received for all assignments.
        """
        studentList = []
        students = self.__students
        for student in students:
            sum = 0
            number = 0
            for grade in self.__grades.getStudentGrades(student):
                if grade.getGrade() is not None:
                    sum += grade.getGrade()
                    number += 1
            average = sum / number if number != 0 else 0
            studentList.append((student, average))
        return sorted(studentList, key=lambda pair: pair[1], reverse=True)

    def getAssignmentsSortedByAverage(self) -> List[Tuple[Assignment, float]]:
        """
        Return a list of tuples consisting of all assignments and their average grades for which there is at least one
        grade, sorted in descending order of the average grade received by all students who received that assignment.
        """
        assignmentList = []
        assignments = self.__assignments
        for assignment in assignments:
            sum = 0
            number = 0
            for grade in self.__grades.getAssignmentGrades(assignment):
                if grade.getGrade() is not None:
                    sum += grade.getGrade()
                    number += 1
            if number != 0:
                average = sum / number
                assignmentList.append((assignment, average))
        return sorted(assignmentList, key=lambda pair: pair[1], reverse=True)

    def getGrade(self, studentId, assignmentId):
        student = self.findStudent(studentId)
        assignment = self.findAssignment(assignmentId)
        return self.__grades[student.getStudentId(), assignment.getAssignmentId()]

    def lateStudents(self) -> List[Student]:
        """
        Returns a list with all students who are late in handing in at least one assignment.
        These are all the students who have an ungraded assignment for which the deadline has passed.
        """
        studentList = []
        for student in self.listStudents():
            ungradedAssignments = self.getStudentUngradedAssignments(student.getStudentId())
            for assignment in ungradedAssignments:
                if self.currentDate > assignment.getDeadline():
                    studentList.append(student)
                    break
        return studentList

    def undo(self):
        """
        Undoes the last operation
        """
        return self.__changesStack.undo()

    def redo(self):
        """
        Reverses the last undo operation
        """
        return self.__changesStack.redo()

    def listGrades(self):
        return self.__grades.getGradeList()

    def clearHistory(self):
        self.__changesStack.clearStack()
