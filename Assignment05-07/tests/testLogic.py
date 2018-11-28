from typing import List
from unittest import TestCase
from repository import Repository
from logic import LogicComponent, ChangesHandler
from logic.ValidationUtils import *


class TestLogicComponent(TestCase):

    def setUp(self):
        self.repository: Repository = Repository()
        self.logicComponent: LogicComponent = LogicComponent(self.repository, date(2018, 11, 18))

    def tearDown(self):
        self.repository = None
        self.logicComponent = None

    def testPopulateRepository(self):
        self.logicComponent.populateRepository()
        self.assertTrue(len(self.logicComponent.listStudents()) != 0)
        self.assertTrue(len(self.logicComponent.listAssignments()) != 0)
        self.assertTrue(len(self.logicComponent.listGrades()) != 0)

    def testAddStudent(self):
        student = self.logicComponent.addStudent('Ricky', '7')
        self.assertTrue(student.getName() == 'Ricky')
        self.assertTrue(student.getGroup() == 7)
        with self.assertRaises(InvalidStudentGroup):
            self.logicComponent.addStudent('Ricky', -8)

    def testParseInt(self):
        self.assertTrue(self.logicComponent.parseInt('8', TypeError) == 8)
        with self.assertRaises(TypeError):
            self.logicComponent.parseInt('blah', TypeError)

    def testRemoveStudent(self):
        oldLength = len(self.logicComponent.listStudents())
        student = self.logicComponent.addStudent('Ricky', '7')
        self.logicComponent.removeStudent(str(student.getStudentId()))
        self.assertTrue(len(self.logicComponent.listStudents()) == oldLength)

        self.populateRepository()
        gradeLength = len(self.logicComponent.listGrades())
        self.logicComponent.removeStudent('1')
        self.assertNotEqual(len(self.logicComponent.listGrades()), gradeLength)

    def testFindStudent(self):
        student = self.logicComponent.addStudent('Ricky', '7')
        studentId = student.getStudentId()
        self.assertTrue(self.logicComponent.findStudent(studentId).getName() == 'Ricky')
        self.assertTrue(self.logicComponent.findStudent(studentId).getGroup() == 7)
        with self.assertRaises(InvalidStudentId):
            self.logicComponent.findStudent('-1')

    def testUpdateStudent(self):
        student = self.logicComponent.addStudent('Ricky', '7')
        studentId = student.getStudentId()
        self.logicComponent.updateStudent(studentId, 'Andy', '11')
        self.assertTrue(self.logicComponent.findStudent(studentId).getName() == 'Andy')
        self.assertTrue(self.logicComponent.findStudent(studentId).getGroup() == 11)

    def testListStudentGrades(self):
        student1 = self.logicComponent.addStudent('Ricky', '7')
        student1Id = student1.getStudentId()
        assignment1 = self.logicComponent.addAssignment('Project1', '2.10.2018')
        assignment1Id = assignment1.getAssignmentId()
        grade1 = self.logicComponent.assignToStudent(student1Id, assignment1Id)
        assignment2 = self.logicComponent.addAssignment('Project2', '3.10.2018')
        assignment2Id = assignment2.getAssignmentId()
        grade2 = self.logicComponent.assignToStudent(student1Id, assignment2Id)
        gradeList = self.logicComponent.listStudentGrades(student1Id)
        self.assertTrue(grade1 in gradeList)
        self.assertTrue(grade2 in gradeList)

    def testAddAssignment(self):
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        self.assertTrue(assignment.getDescription() == 'Project')
        self.assertTrue(assignment.getDeadline() == date(2018, 10, 2))
        with self.assertRaises(InvalidAssignmentDeadline):
            self.logicComponent.addAssignment('Project', "-9")

    def testParseDate(self):
        self.assertTrue(self.logicComponent.parseDate('2.10.2018', TypeError) == date(2018, 10, 2))
        with self.assertRaises(TypeError):
            self.logicComponent.parseDate('8', TypeError)
        with self.assertRaises(TypeError):
            self.logicComponent.parseDate('8.-7.432', TypeError)

    def testRemoveAssignment(self):
        oldLength = len(self.logicComponent.listAssignments())
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        self.logicComponent.removeAssignment(str(assignment.getAssignmentId()))
        self.assertTrue(len(self.logicComponent.listAssignments()) == oldLength)

        self.populateRepository()
        gradeLength = len(self.logicComponent.listGrades())
        self.logicComponent.removeAssignment('1')
        self.assertNotEqual(len(self.logicComponent.listGrades()), gradeLength)

    def testFindAssignment(self):
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        assignmentId = assignment.getAssignmentId()
        self.assertTrue(self.logicComponent.findAssignment(assignmentId).getDescription() == 'Project')
        self.assertTrue(self.logicComponent.findAssignment(assignmentId).getDeadline() == date(2018, 10, 2))
        with self.assertRaises(InvalidAssignmentId):
            self.logicComponent.findAssignment('-1')

    def testUpdateAssignment(self):
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        assignmentId = assignment.getAssignmentId()
        self.logicComponent.updateAssignment(assignmentId, 'Project 2', '2.11.2018')
        self.assertTrue(self.logicComponent.findAssignment(assignmentId).getDescription() == 'Project 2')
        self.assertTrue(self.logicComponent.findAssignment(assignmentId).getDeadline() == date(2018, 11, 2))

    def testListAssignmentGrades(self):
        student1 = self.logicComponent.addStudent('Ricky', '7')
        student1Id = student1.getStudentId()
        student2 = self.logicComponent.addStudent('Michael', '8')
        student2Id = student2.getStudentId()
        assignment1 = self.logicComponent.addAssignment('Project1', '2.10.2018')
        assignment1Id = assignment1.getAssignmentId()
        grade1 = self.logicComponent.assignToStudent(student1Id, assignment1Id)
        grade2 = self.logicComponent.assignToStudent(student2Id, assignment1Id)
        gradeList = self.logicComponent.listAssignmentGrades(assignment1Id)
        self.assertTrue(grade1 in gradeList)
        self.assertTrue(grade2 in gradeList)

    def testAssignToStudent(self):
        student = self.logicComponent.addStudent('Ricky', '7')
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        self.assertTrue(len(self.repository.getGrades().getStudentGrades(student)) == 0)
        self.assertTrue(len(self.repository.getGrades().getAssignmentGrades(assignment)) == 0)
        self.logicComponent.assignToStudent(student.getStudentId(), assignment.getAssignmentId())
        self.assertTrue(len(self.repository.getGrades().getStudentGrades(student)) == 1)
        self.assertTrue(len(self.repository.getGrades().getAssignmentGrades(assignment)) == 1)
        self.assertTrue(self.repository.getGrades()[student.getStudentId(), assignment.getAssignmentId()] is not None)

    def testCheckGroupExistence(self):
        group = 0
        # while group in [student.getGroup() for student in self.repository.getStudents()]:
        #     group += 1
        self.logicComponent.addStudent('Ricky', group)
        self.logicComponent.checkGroupExistence(group)
        while group in [student.getGroup() for student in self.repository.getStudents()]:
            group += 1
        with self.assertRaises(InvalidStudentGroup):
            self.logicComponent.checkGroupExistence(group)

    def testAssignToGroup(self):
        group = 0
        # while group in [student.getGroup() for student in self.repository.getStudents()]:
        #     group += 1
        student1 = self.logicComponent.addStudent('Ricky', group)
        student2 = self.logicComponent.addStudent('Alfred', group)
        student3 = self.logicComponent.addStudent('Alex', group)
        assignment = self.logicComponent.addAssignment('Project', '2.10.2018')
        self.logicComponent.assignToStudent(student1.getStudentId(), assignment.getAssignmentId())
        self.logicComponent.assignToGroup(group, assignment.getAssignmentId())
        self.assertTrue(self.repository.getGrades()[student1.getStudentId(), assignment.getAssignmentId()] is not None)
        self.assertTrue(self.repository.getGrades()[student2.getStudentId(), assignment.getAssignmentId()] is not None)
        self.assertTrue(self.repository.getGrades()[student3.getStudentId(), assignment.getAssignmentId()] is not None)

    def testGrade(self):
        student1 = self.logicComponent.addStudent('Ricky', '7')
        student1Id = student1.getStudentId()
        assignment1 = self.logicComponent.addAssignment('Project1', '2.10.2018')
        assignment1Id = assignment1.getAssignmentId()
        with self.assertRaises(InvalidAssignmentId):
            self.logicComponent.grade(student1Id, assignment1Id, '1')
        grade = self.logicComponent.assignToStudent(student1Id, assignment1Id)
        with self.assertRaises(InvalidGrade):
            self.logicComponent.grade(student1Id, assignment1Id, '-1')
        with self.assertRaises(InvalidAssignmentId):
            self.logicComponent.grade(student1Id, '-1', '1')
        self.logicComponent.grade(student1Id, assignment1Id, '10')
        self.assertEqual(grade.getGrade(), 10)
        with self.assertRaises(InvalidAssignmentId):
            self.logicComponent.grade(student1Id, assignment1Id, '1')

    def testGetStudentUngradedAssignments(self):
        student1 = self.logicComponent.addStudent('Ricky', '7')
        student1Id = student1.getStudentId()
        assignment1 = self.logicComponent.addAssignment('Project1', '2.10.2018')
        assignment1Id = assignment1.getAssignmentId()
        assignment2 = self.logicComponent.addAssignment('Project2', '3.10.2018')
        assignment2Id = assignment2.getAssignmentId()
        grade1 = self.logicComponent.assignToStudent(student1Id, assignment1Id)
        grade2 = self.logicComponent.assignToStudent(student1Id, assignment2Id)
        self.logicComponent.grade(student1Id, assignment1Id, '7')
        assignmentList = self.logicComponent.getStudentUngradedAssignments(student1Id)
        self.assertTrue(assignment2 in assignmentList)

    def testAssignmentGradable(self):
        student1 = self.logicComponent.addStudent('Ricky', '7')
        student1Id = student1.getStudentId()
        assignment1 = self.logicComponent.addAssignment('Project1', '2.10.2018')
        assignment1Id = assignment1.getAssignmentId()
        with self.assertRaises(InvalidAssignmentId):
            self.logicComponent.assignmentGradable(student1Id, assignment1Id)
        self.logicComponent.assignToStudent(student1Id, assignment1Id)
        self.logicComponent.assignmentGradable(student1Id, assignment1Id)
        self.logicComponent.grade(student1Id, assignment1Id, '9')
        with self.assertRaises(InvalidAssignmentId):
            self.logicComponent.assignmentGradable(student1Id, assignment1Id)

    def populateRepository(self):
        studentList: List[Student] = [
            self.logicComponent.addStudent('Andrew', 915),
            self.logicComponent.addStudent('Richard', 915),
            self.logicComponent.addStudent('John', 917),
            self.logicComponent.addStudent('Hori', 917)
        ]
        assignmentList: List[Assignment] = [
            self.logicComponent.addAssignment('Assignment 01', "10.10.2018"),
            self.logicComponent.addAssignment('Assignment 02', "17.10.2018"),
            self.logicComponent.addAssignment('Assignment 03-04', "31.10.2018"),
            self.logicComponent.addAssignment('Assignment 05-07', "28.11.2018")
        ]

        self.logicComponent.assignToStudent(studentList[0].getStudentId(),
                                            assignmentList[1].getAssignmentId()).setGrade(10)
        self.logicComponent.assignToStudent(studentList[0].getStudentId(), assignmentList[3].getAssignmentId())
        self.logicComponent.assignToStudent(studentList[1].getStudentId(),
                                            assignmentList[1].getAssignmentId()).setGrade(5)
        self.logicComponent.assignToStudent(studentList[1].getStudentId(),
                                            assignmentList[2].getAssignmentId()).setGrade(4)
        self.logicComponent.assignToStudent(studentList[2].getStudentId(), assignmentList[2].getAssignmentId())
        self.logicComponent.assignToStudent(studentList[2].getStudentId(),
                                            assignmentList[3].getAssignmentId()).setGrade(9)
        self.logicComponent.assignToStudent(studentList[3].getStudentId(), assignmentList[1].getAssignmentId())
        self.logicComponent.clearHistory()

    def testGetStudentsForAssignmentSortedAlphabetically(self):
        self.populateRepository()
        student = self.logicComponent.findStudent
        output = [student(0), student(3), student(1)]
        self.assertEqual(output, self.logicComponent.getStudentsForAssignmentSortedAlphabetically('1'))

    def testGetStudentsForAssignmentSortedByGrade(self):
        self.populateRepository()
        student = self.logicComponent.findStudent
        output = [student(0), student(1), student(3)]
        self.assertEqual(output, self.logicComponent.getStudentsForAssignmentSortedByGrade('1'))

    def testGetStudentsSortedByAverage(self):
        self.populateRepository()
        student = self.logicComponent.findStudent
        output = [(student(0), 10), (student(2), 9), (student(1), 4.5), (student(3), 0)]
        self.assertEqual(output, self.logicComponent.getStudentsSortedByAverage())

    def testGetAssignmentsSortedByAverage(self):
        self.populateRepository()
        assignment = self.logicComponent.findAssignment
        output = [(assignment(3), 9), (assignment(1), 7.5), (assignment(2), 4)]
        self.assertEqual(output, self.logicComponent.getAssignmentsSortedByAverage())

    def testGetGrade(self):
        student1 = self.logicComponent.addStudent('Ricky', '7')
        student1Id = student1.getStudentId()
        assignment1 = self.logicComponent.addAssignment('Project1', '2.10.2018')
        assignment1Id = assignment1.getAssignmentId()
        grade = self.logicComponent.assignToStudent(student1Id, assignment1Id)
        self.assertEqual(grade, self.logicComponent.getGrade(student1Id, assignment1Id))

    def testLateStudents(self):
        self.populateRepository()
        student = self.logicComponent.findStudent
        output = [student(2), student(3)]
        self.assertEqual(output, self.logicComponent.lateStudents())

    def testUndoRedo(self):
        self.populateRepository()

        studentNumber = len(self.logicComponent.listStudents())
        self.logicComponent.addStudent("Sample Name", '67')
        self.assertEqual(len(self.logicComponent.listStudents()), studentNumber + 1)
        self.logicComponent.undo()
        self.assertEqual(len(self.logicComponent.listStudents()), studentNumber)
        self.logicComponent.undo()
        self.assertEqual(len(self.logicComponent.listStudents()), studentNumber)
        self.logicComponent.redo()
        self.assertEqual(len(self.logicComponent.listStudents()), studentNumber + 1)
        self.logicComponent.redo()
        self.assertEqual(len(self.logicComponent.listStudents()), studentNumber + 1)
        self.logicComponent.clearHistory()

        gradeNumber = len(self.logicComponent.listGrades())
        self.logicComponent.assignToStudent('1', '0')
        self.assertEqual(len(self.logicComponent.listGrades()), gradeNumber + 1)
        self.logicComponent.undo()
        self.assertEqual(len(self.logicComponent.listGrades()), gradeNumber)
        self.logicComponent.undo()
        self.assertEqual(len(self.logicComponent.listGrades()), gradeNumber)
        self.logicComponent.redo()
        self.assertEqual(len(self.logicComponent.listGrades()), gradeNumber + 1)
        self.logicComponent.redo()
        self.assertEqual(len(self.logicComponent.listGrades()), gradeNumber + 1)
        self.logicComponent.clearHistory()

        assignmentNumber = len(self.logicComponent.listAssignments())
        self.logicComponent.addAssignment("Sample description", '6.7.2018')
        self.assertEqual(len(self.logicComponent.listAssignments()), assignmentNumber + 1)
        self.logicComponent.undo()
        self.assertEqual(len(self.logicComponent.listAssignments()), assignmentNumber)
        self.logicComponent.undo()
        self.assertEqual(len(self.logicComponent.listAssignments()), assignmentNumber)
        self.logicComponent.redo()
        self.assertEqual(len(self.logicComponent.listAssignments()), assignmentNumber + 1)
        self.logicComponent.redo()
        self.assertEqual(len(self.logicComponent.listAssignments()), assignmentNumber + 1)
        self.logicComponent.clearHistory()

    def testChangesHandlerAbstract(self):
        ChangesHandler().handleChanges([], True)
