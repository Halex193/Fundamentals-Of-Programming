from unittest import TestCase

from main import Backtracker, solution, valid, buildPrimeNumbers


class TestBacktracker(TestCase):
    def setUp(self):
        self.backtracker = Backtracker(solution, None, valid)

    def testRecursive(self):
        number = 13
        entities = buildPrimeNumbers(number)
        self.backtracker.entities = entities
        result = self.backtracker.recursive(number)
        self.assertIn([13], result)
        self.assertIn([2, 2, 2, 2, 5], result)
        self.assertIn([2, 3, 3, 5], result)
        self.assertIn([2, 11], result)

        number = 2
        entities = buildPrimeNumbers(number)
        self.backtracker.entities = entities
        result = self.backtracker.recursive(number)
        self.assertIn([2], result)

    def testIterative(self):
        number = 13
        entities = buildPrimeNumbers(number)
        self.backtracker.entities = entities
        result = self.backtracker.iterative(number)
        self.assertIn([13], result)
        self.assertIn([2, 2, 2, 2, 5], result)
        self.assertIn([2, 3, 3, 5], result)
        self.assertIn([2, 11], result)

        number = 2
        entities = buildPrimeNumbers(number)
        self.backtracker.entities = entities
        result = self.backtracker.iterative(number)
        self.assertIn([2], result)
