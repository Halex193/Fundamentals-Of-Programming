import datetime
import random
from copy import copy
from typing import List

from logic.ControllerWrapper import ControllerWrapper
from logic.ValidationUtils import ValidationUtils, InvalidAssignmentId
from model.Assignment import Assignment
from repository.Repository import Repository


class AssignmentController:

    def __init__(self, assignmentRepository: Repository, controllerWrapper: ControllerWrapper):
        self.__assignmentRepository = assignmentRepository
        self.__controllerWrapper = controllerWrapper

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
        ValidationUtils.Assignment.validateAssignment(assignment)
        self.__assignmentRepository.addItem(assignment)
        self.__controllerWrapper.itemAdded(assignment)

        return assignment

    def removeAssignment(self, assignmentId: int):
        """
        Removes an assignment from the repository
        """
        assignment = self.findAssignment(assignmentId)
        self.__assignmentRepository.deleteItem(assignment)
        self.__controllerWrapper.itemRemoved(assignment)

    def findAssignment(self, assignmentId: int) -> Assignment:
        """
        Searches an assignment and returns it if found. Raises InvalidAssignmentId otherwise
        """
        assignment = Assignment(assignmentId)
        foundAssignment = self.__assignmentRepository.getItem(assignment)
        if foundAssignment is None:
            raise InvalidAssignmentId
        return foundAssignment

    def updateAssignment(self, assignmentId: int, description: str, deadline: datetime.date):
        """
        Updates the assignment data
        """
        assignment = self.findAssignment(assignmentId)
        newAssignment = copy(assignment)
        newAssignment.setDescription(description)
        newAssignment.setDeadline(deadline)
        ValidationUtils.Assignment.validateAssignment(newAssignment)
        self.__assignmentRepository.updateItem(newAssignment)
        self.__controllerWrapper.itemUpdated(assignment, newAssignment)

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
