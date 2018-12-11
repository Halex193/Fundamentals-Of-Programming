from unittest import TestCase

from repository.Repository import Repository
from repository.RepositoryError import *


class TestRepository(TestCase):

    def setUp(self):
        self.repository = Repository(int)

    def tearDown(self):
        self.repository = None

    def testCreate(self):
        self.assertEqual(len(self.repository.getItems()), 0)

    def testAdd(self):
        self.repository.addItem(3)
        self.assertEqual(len(self.repository.getItems()), 1)
        self.repository.addItem(4)
        self.assertEqual(len(self.repository.getItems()), 2)
        with self.assertRaises(DuplicateItemError):
            self.repository.addItem(3)

    def testDelete(self):
        self.repository.addItem(6)
        with self.assertRaises(ItemNotFoundError):
            self.repository.deleteItem(8)
        self.assertEqual(len(self.repository.getItems()), 1)
        self.repository.deleteItem(6)
        self.assertEqual(len(self.repository.getItems()), 0)

    def testRead(self):
        self.repository.addItem(6)
        self.assertEqual(self.repository.getItem(6), 6)

    def testUpdate(self):
        self.repository.addItem(6)
        self.repository.updateItem(6)
        self.assertEqual(len(self.repository.getItems()), 1)
