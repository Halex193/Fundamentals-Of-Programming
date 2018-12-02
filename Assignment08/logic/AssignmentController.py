import datetime
import random
from copy import copy
from typing import List

from logic.ChangesStack import ChangesStack
from logic.ControllerError import AssignmentIdNotFound
from model.Assignment import Assignment
from model.ValidationError import InvalidAssignmentId
from model.Validators import AssignmentValidator
from repository.Repository import Repository


class AssignmentController:

    def __init__(self, assignmentRepository: Repository, changesStack: ChangesStack):
        self.__assignmentRepository = assignmentRepository
        self.__changesStack = changesStack

    def listAssignments(self) -> List[Assignment]:
        """
        Returns a list of assignments sorted in ascending order by their IDs
        """
        return sorted(self.__assignmentRepository.getItems(), key=lambda assignment: assignment.getAssignmentId())

    def addAssignment(self, assignmentId: int, description: str, deadline: datetime.date) -> Assignment:
        """
        Adds an assignment to the repository
        """
        assignment = Assignment(assignmentId, description, deadline)
        AssignmentValidator.validateAssignment(assignment)
        self.__assignmentRepository.addItem(assignment)
        self.__changesStack.addChange(ChangesStack.ItemAdded(assignment), newCommit=True)

        return assignment

    def removeAssignment(self, assignmentId: int, deleteCallback: function = None):
        """
        Removes an assignment from the repository
        """
        assignment = self.findAssignment(assignmentId)
        self.__assignmentRepository.deleteItem(assignment)
        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(assignment))
        if deleteCallback is not None:
            deleteCallback(assignment)
        else:
            self.__changesStack.endCommit()

    def findAssignment(self, assignmentId: int) -> Assignment:
        """
        Searches an assignment and returns it if found. Raises InvalidAssignmentId otherwise
        """
        assignment = Assignment(assignmentId)
        foundAssignment = self.__assignmentRepository.getItem(assignment)
        if foundAssignment is None:
            raise AssignmentIdNotFound
        return foundAssignment

    def updateAssignment(self, assignmentId: int, description: str, deadline: datetime.date):
        """
        Updates the assignment data
        """
        assignment = self.findAssignment(assignmentId)
        newAssignment = copy(assignment)
        newAssignment.setDescription(description)
        newAssignment.setDeadline(deadline)
        AssignmentValidator.validateAssignment(newAssignment)
        self.__assignmentRepository.updateItem(newAssignment)

        self.__changesStack.beginCommit()
        self.__changesStack.addChange(ChangesStack.ItemRemoved(assignment))
        self.__changesStack.addChange(ChangesStack.ItemAdded(newAssignment))
        self.__changesStack.endCommit()

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

            assignmentDate = self.randomDate(datetime.date(2018, 1, 1), datetime.date(2020, 1, 1))
            self.addAssignment(i, description, assignmentDate)

    @staticmethod
    def randomDate(start, end):
        """
        Generate a random datetime between `start` and `end`
        """
        return start + datetime.timedelta(
            # Get a random amount of seconds between `start` and `end`
            seconds=random.randint(0, int((end - start).total_seconds())),
        )
