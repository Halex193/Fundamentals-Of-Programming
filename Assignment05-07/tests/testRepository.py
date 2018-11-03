from unittest import TestCase
from repository import *
from model import *


class TestRepository(TestCase):

    def setUp(self):
        self.repository = Repository()
        self.students = self.repository.getStudents()
        self.grades = self.repository.getGrades()
        self.assignments = self.repository.getAssignments()

    def testCreate(self):
        assert self.students is not None
        assert self.grades is not None
        assert self.assignments is not None
        assert len(self.students) == 0
        assert len(self.grades) == 0
        assert len(self.assignments) == 0

    def testDelete(self):
        student1 = self.students.addStudent(Student(0, 'Andrew'))
        assignment1 = self.assignments.addAssignment(Assignment(0, 'Project', date(1999, 8, 9)))
        student2 = self.students.addStudent(Student(0, 'Jamie'))
        assignment2 = self.assignments.addAssignment(Assignment(0, 'Project 2', date(1999, 10, 10)))
        self.grades.assign(student1, assignment1)
        self.grades.assign(student1, assignment2)
        assert len(self.grades) == 2
        assert len(self.grades.getStudentGrades(student1)) == 2
        assert len(self.grades.getAssignmentGrades(assignment1)) == 1

        del self.students[student1]
        assert len(self.grades) == 0

        self.grades.assign(student1, assignment1)
        self.grades.assign(student2, assignment1)
        assert len(self.grades) == 2
        assert len(self.grades.getStudentGrades(student1)) == 1
        assert len(self.grades.getAssignmentGrades(assignment1)) == 2

        del self.assignments[assignment1]
        assert len(self.grades) == 0


class TestStudentCollection(TestCase):

    def setUp(self):
        self.students = StudentCollection()
        self.students.addStudent(Student(0, 'Robert'))
        self.students.addStudent(Student(0, 'Alex', 25))
        self.students.addStudent(Student(0, 'Richard', 4))
        self.students.addStudent(Student(0, 'Paul'))

    def testCRUD(self):
        assert len(self.students) == 4
        robert: Student = None
        richard: Student = None
        for student in self.students:
            if student.getName() == 'Robert':
                robert = student
            if student.getName() == 'Richard':
                richard = student
        assert robert is not None
        assert richard is not None
        assert robert == self.students[robert.getStudentId()]
        assert richard == self.students[richard.getStudentId()]
        assert self.students[-1] is None
        assert robert in self.students
        assert richard in self.students
        del self.students[robert]
        assert robert not in self.students
        del self.students[richard]
        assert richard not in self.students
        self.assertRaises(KeyError, TestStudentCollection.deleteStudent, self, robert)
        self.assertRaises(KeyError, TestStudentCollection.deleteStudent, self, richard)

    def deleteStudent(self, student):
        del self.students[student]


class TestGradeCollection(TestCase):

    def setUp(self):
        self.grades = GradeCollection()
        self.student1 = Student(1, 'John')
        self.student2 = Student(2, 'Ana')
        self.assignment1 = Assignment(2, 'Project 1', date(2018, 7, 6))
        self.assignment2 = Assignment(3, 'Project 2', date(2018, 6, 6))

    def testCRUD(self):
        self.grades.assign(self.student1, self.assignment1)
        assert len(self.grades.getStudentGrades(self.student1)) == 1
        assert len(self.grades.getAssignmentGrades(self.assignment1)) == 1
        grade = self.grades[(self.student1.getStudentId(), self.assignment1.getAssignmentId())]
        grade.setGrade(10)
        assert self.grades.getStudentGrades(self.student1)[0] == self.grades.getAssignmentGrades(self.assignment1)[0]
        assert self.grades.getStudentGrades(self.student1)[0].getGrade() == 10
        assert len(self.grades) == 1

        self.assertRaises(KeyError, self.grades.assign, self.student1, self.assignment1)
        self.grades.assign(self.student2, self.assignment2)
        assert len(self.grades.getStudentGrades(self.student2)) == 1
        assert len(self.grades.getAssignmentGrades(self.assignment2)) == 1
        assert len(self.grades) == 2

        self.grades.assign(self.student1, self.assignment2)
        assert len(self.grades.getStudentGrades(self.student1)) == 2
        assert len(self.grades.getAssignmentGrades(self.assignment2)) == 2
        assert len(self.grades) == 3

        self.grades.assign(self.student2, self.assignment1)
        assert len(self.grades.getStudentGrades(self.student2)) == 2
        assert len(self.grades.getAssignmentGrades(self.assignment1)) == 2
        assert len(self.grades) == 4

        del self.grades[grade]
        assert len(self.grades.getStudentGrades(self.student1)) == 1
        self.assertRaises(KeyError, TestGradeCollection.deleteGrade, self, grade)
        
        assert self.grades[(14,15)] is None

    def deleteGrade(self, grade):
        del self.grades[grade]


class TestAssignmentCollection(TestCase):

    def setUp(self):
        self.assignments = AssignmentCollection()
        self.assignments.addAssignment(Assignment(0, 'Project 1', date(2018, 9, 8)))
        self.assignments.addAssignment(Assignment(0, 'Project 2', date(2018, 10, 8)))
        self.assignments.addAssignment(Assignment(0, 'Project 3', date(2018, 11, 7)))
        self.assignments.addAssignment(Assignment(0, 'Project 4', date(2018, 12, 9)))

    def testCRUD(self):
        assert len(self.assignments) == 4
        assignment2: Assignment = None
        assignment3: Assignment = None
        for assignment in self.assignments:
            if assignment.getDescription() == 'Project 2':
                assignment2 = assignment
            if assignment.getDescription() == 'Project 3':
                assignment3 = assignment
        assert assignment2 is not None
        assert assignment3 is not None
        assert assignment2 == self.assignments[assignment2.getAssignmentId()]
        assert assignment3 == self.assignments[assignment3.getAssignmentId()]
        assert self.assignments[-1] is None
        assert assignment2 in self.assignments
        assert assignment3 in self.assignments
        del self.assignments[assignment2]
        assert assignment2 not in self.assignments
        del self.assignments[assignment3]
        assert assignment3 not in self.assignments
        self.assertRaises(KeyError, TestAssignmentCollection.deleteAssignment, self, assignment2)
        self.assertRaises(KeyError, TestAssignmentCollection.deleteAssignment, self, assignment3)

    def deleteAssignment(self, assignment):
        del self.assignments[assignment]
