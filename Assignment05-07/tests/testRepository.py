from unittest import TestCase
from repository import *
from model import *


class TestRepository(TestCase):

    def setUp(self):
        self.repository = Repository()
        self.students = self.repository.getStudents()
        self.grades = self.repository.getGrades()
        self.assignments = self.repository.getAssignments()

    def tearDown(self):
        self.repository = None
        self.students = None
        self.grades = None
        self.assignments = None

    def testCreate(self):
        self.assertTrue(self.students is not None)
        self.assertTrue(self.grades is not None)
        self.assertTrue(self.assignments is not None)
        self.assertTrue(len(self.students) == 0)
        self.assertTrue(len(self.grades) == 0)
        self.assertTrue(len(self.assignments) == 0)

    def testDelete(self):
        student1 = self.students.addStudent(Student(0, 'Andrew'))
        assignment1 = self.assignments.addAssignment(Assignment(0, 'Project', date(1999, 8, 9)))
        student2 = self.students.addStudent(Student(0, 'Jamie'))
        assignment2 = self.assignments.addAssignment(Assignment(0, 'Project 2', date(1999, 10, 10)))
        self.grades.assign(student1, assignment1)
        self.grades.assign(student1, assignment2)
        self.assertTrue(len(self.grades) == 2)
        self.assertTrue(len(self.grades.getStudentGrades(student1)) == 2)
        self.assertTrue(len(self.grades.getAssignmentGrades(assignment1)) == 1)

        del self.students[student1]
        self.assertTrue(len(self.grades) == 0)

        self.grades.assign(student1, assignment1)
        self.grades.assign(student2, assignment1)
        self.assertTrue(len(self.grades) == 2)
        self.assertTrue(len(self.grades.getStudentGrades(student1)) == 1)
        self.assertTrue(len(self.grades.getAssignmentGrades(assignment1)) == 2)

        del self.assignments[assignment1]
        self.assertTrue(len(self.grades) == 0)


class TestStudentCollection(TestCase):

    def setUp(self):
        self.students = StudentCollection()
        self.students.addStudent(Student(0, 'Robert'))
        self.students.addStudent(Student(0, 'Alex', 25))
        self.students.addStudent(Student(0, 'Richard', 4))
        self.students.addStudent(Student(0, 'Paul'))

    def tearDown(self):
        self.students = None

    def testCRUD(self):
        self.assertTrue(len(self.students) == 4)
        robert: Student = None
        richard: Student = None
        for student in self.students:
            if student.getName() == 'Robert':
                robert = student
            if student.getName() == 'Richard':
                richard = student
        self.assertTrue(robert is not None)
        self.assertTrue(richard is not None)
        self.assertTrue(robert == self.students[robert.getStudentId()])
        self.assertTrue(richard == self.students[richard.getStudentId()])
        self.assertTrue(self.students[-1] is None)
        self.assertTrue(robert in self.students)
        self.assertTrue(richard in self.students)
        del self.students[robert]
        self.assertTrue(robert not in self.students)
        del self.students[richard]
        self.assertTrue(richard not in self.students)
        with self.assertRaises(KeyError):
            del self.students[robert]
        with self.assertRaises(KeyError):
            del self.students[richard]


class TestGradeCollection(TestCase):

    def setUp(self):
        self.grades = GradeCollection()
        self.student1 = Student(1, 'John')
        self.student2 = Student(2, 'Ana')
        self.assignment1 = Assignment(2, 'Project 1', date(2018, 7, 6))
        self.assignment2 = Assignment(3, 'Project 2', date(2018, 6, 6))

    def tearDown(self):
        self.grades = None
        self.student1 = None
        self.student2 = None
        self.assignment1 = None
        self.assignment2 = None

    def testCRUD(self):
        self.grades.assign(self.student1, self.assignment1)
        self.assertTrue(len(self.grades.getStudentGrades(self.student1)) == 1)
        self.assertTrue(len(self.grades.getAssignmentGrades(self.assignment1)) == 1)
        grade = self.grades[(self.student1.getStudentId(), self.assignment1.getAssignmentId())]
        grade.setGrade(10)
        self.assertTrue(
            self.grades.getStudentGrades(self.student1)[0] == self.grades.getAssignmentGrades(self.assignment1)[0])
        self.assertTrue(self.grades.getStudentGrades(self.student1)[0].getGrade() == 10)
        self.assertTrue(len(self.grades) == 1)

        with self.assertRaises(KeyError):
            self.grades.assign(self.student1, self.assignment1)
        self.grades.assign(self.student2, self.assignment2)
        self.assertTrue(len(self.grades.getStudentGrades(self.student2)) == 1)
        self.assertTrue(len(self.grades.getAssignmentGrades(self.assignment2)) == 1)
        self.assertTrue(len(self.grades) == 2)

        self.grades.assign(self.student1, self.assignment2)
        self.assertTrue(len(self.grades.getStudentGrades(self.student1)) == 2)
        self.assertTrue(len(self.grades.getAssignmentGrades(self.assignment2)) == 2)
        self.assertTrue(len(self.grades) == 3)

        self.grades.assign(self.student2, self.assignment1)
        self.assertTrue(len(self.grades.getStudentGrades(self.student2)) == 2)
        self.assertTrue(len(self.grades.getAssignmentGrades(self.assignment1)) == 2)
        self.assertTrue(len(self.grades) == 4)

        del self.grades[grade]
        self.assertTrue(len(self.grades.getStudentGrades(self.student1)) == 1)
        with self.assertRaises(KeyError):
            del self.grades[grade]
        self.assertTrue(self.grades[(14, 15)] is None)


class TestAssignmentCollection(TestCase):

    def setUp(self):
        self.assignments = AssignmentCollection()
        self.assignments.addAssignment(Assignment(0, 'Project 1', date(2018, 9, 8)))
        self.assignments.addAssignment(Assignment(0, 'Project 2', date(2018, 10, 8)))
        self.assignments.addAssignment(Assignment(0, 'Project 3', date(2018, 11, 7)))
        self.assignments.addAssignment(Assignment(0, 'Project 4', date(2018, 12, 9)))

    def tearDown(self):
        self.assignments = None

    def testCRUD(self):
        self.assertTrue(len(self.assignments) == 4)
        assignment2: Assignment = None
        assignment3: Assignment = None
        for assignment in self.assignments:
            if assignment.getDescription() == 'Project 2':
                assignment2 = assignment
            if assignment.getDescription() == 'Project 3':
                assignment3 = assignment
        self.assertTrue(assignment2 is not None)
        self.assertTrue(assignment3 is not None)
        self.assertTrue(assignment2 == self.assignments[assignment2.getAssignmentId()])
        self.assertTrue(assignment3 == self.assignments[assignment3.getAssignmentId()])
        self.assertTrue(self.assignments[-1] is None)
        self.assertTrue(assignment2 in self.assignments)
        self.assertTrue(assignment3 in self.assignments)
        del self.assignments[assignment2]
        self.assertTrue(assignment2 not in self.assignments)
        del self.assignments[assignment3]
        self.assertTrue(assignment3 not in self.assignments)
        with self.assertRaises(KeyError):
            del self.assignments[assignment2]
        with self.assertRaises(KeyError):
            del self.assignments[assignment3]
