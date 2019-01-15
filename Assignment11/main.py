# Udrea Horațiu 917
from copy import deepcopy
from math import sqrt


class Backtracker:
    """
    Wrapper class for backtracking algorithm
    """
    def __init__(self, solution, entities, valid):
        self.solution = solution
        self.entities = entities
        self.valid = valid
        self.list = None
        self.resultCollection = None
        self.number = None

    def recursive(self, number):
        """
        Recursive backtracking wrapper method
        """
        self.list = []
        self.resultCollection = []
        self.number = number
        self.recursiveBacktracking(0)
        return self.resultCollection

    def recursiveBacktracking(self, step):
        """
        Recursive backtracking method
        :param step: The current step
        """
        self.list.append(None)
        for i in range(len(self.entities)):
            self.list[-1] = self.entities[i]
            if self.valid(self.list, self.number):
                if solution(self.list, self.number):
                    self.resultCollection.append(deepcopy(self.list))
                else:
                    self.recursiveBacktracking(step + 1)

        self.list.pop()

    def iterative(self, number):
        """
        Iterative backtracking method
        """
        self.list = []
        self.resultCollection = []
        self.number = number

        self.list.append(None)
        step = 0
        while step >= 0:
            if self.list[-1] is None:
                self.list[-1] = self.entities[0]
            else:
                index = self.entities.index(self.list[-1])
                if index == len(self.entities) - 1:
                    step -= 1
                    self.list.pop()
                    continue
                self.list[-1] = self.entities[index + 1]
            if self.valid(self.list, self.number):
                if self.solution(self.list, self.number):
                    self.resultCollection.append(deepcopy(self.list))
                else:
                    step += 1
                    self.list.append(None)
        return self.resultCollection

    @staticmethod
    def formatResult(resultCollection):
        """
        Result formatter. Converts the list of results to a string
        """
        return '\n'.join([', '.join([str(integer) for integer in solution]) for solution in resultCollection])


def isPrime(number):
    """
    Checks if a number is prime
    """
    if number <= 1:
        return False

    if number == 2:
        return True

    if number % 2 == 0:
        return False

    for divisor in range(3, int(sqrt(number)), 2):
        if number % divisor == 0:
            return False

    return True


def buildPrimeNumbers(number):
    """
    Builds a list of prime numbers smaller than the given number
    """
    primeNumberList = []
    for i in range(2, number + 1):
        if isPrime(i):
            primeNumberList.append(i)

    return primeNumberList


def solution(currentList, number):
    """
    Checks if the given list represents a solution
    """
    return sum(currentList) == number


def valid(currentList, number):
    """
    Checks if the current list provides elements tht will be able to form a solution
    """
    if len(currentList) >= 2 and currentList[-1] < currentList[-2]:
        return False
    return sum(currentList) <= number


if __name__ == '__main__':
    validInput = False
    number = 0
    while not validInput:
        try:
            number = int(input("Choose the number: "))
            if number <= 1:
                raise ValueError
            validInput = True
        except ValueError:
            print("Please provide a valid number")

    entities = buildPrimeNumbers(number)
    backtracker = Backtracker(solution, entities, valid)

    recursiveResult = backtracker.recursive(number)
    recursiveOutput = Backtracker.formatResult(recursiveResult)
    print("Recursive solution:\n{}".format(recursiveOutput))
    print()
    iterativeResult = backtracker.iterative(number)
    iterativeOutput = Backtracker.formatResult(iterativeResult)
    print("Iterative solution:\n{}".format(iterativeOutput))
