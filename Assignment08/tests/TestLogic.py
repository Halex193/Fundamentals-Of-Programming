from unittest import TestCase

from logic.ControllerWrapper import ControllerWrapper
from model.Validators import *
from repository import Repository
from repository.RepositoryWrapper import RepositoryWrapper


class TestControllers(TestCase):

    def setUp(self):
        self.repositoryWrapper: Repository = RepositoryWrapper("inmemory", '', '', '')
        self.controllerWrapper: ControllerWrapper = ControllerWrapper(self.repositoryWrapper, date(2018, 11, 18))
        self.studentController = self.controllerWrapper.getStudentController()
        self.gradeController = self.controllerWrapper.getGradeController()
        self.assignmentController = self.controllerWrapper.getAssignmentController()

    def tearDown(self):
        self.repositoryWrapper = None
        self.controllerWrapper: None
        self.studentController = None
        self.gradeController = None
        self.assignmentController = None

    # def testPopulateRepository(self):
    #     self.controllerWrapper.populateRepository()
    #     self.assertTrue(len(self.studentController.listStudents()) != 0)
    #     self.assertTrue(len(self.assignmentController.listAssignments()) != 0)
    #     self.assertTrue(len(self.gradeController.listGrades()) != 0)
    #
    # def testAddStudent(self):
    #     student = self.studentController.addStudent(1, 'Ricky', 7)
    #     self.assertTrue(student.getName() == 'Ricky')
    #     self.assertTrue(student.getGroup() == 7)
    #     with self.assertRaises(InvalidStudentGroup):
    #         self.studentController.addStudent(2, 'Ricky', -8)
    #
    # def testParseInt(self):
    #     self.assertTrue(TypeParser.parseInt('8', TypeError) == 8)
    #     with self.assertRaises(TypeError):
    #         TypeParser.parseInt('blah', TypeError)
    #
    # def testRemoveStudent(self):
    #     oldLength = len(self.studentController.listStudents())
    #     student = self.studentController.addStudent(1, 'Ricky', '7')
    #     self.studentController.removeStudent(str(student.getStudentId()))
    #     self.assertTrue(len(self.studentController.listStudents()) == oldLength)
    #
    #     self.populateRepository()
    #     gradeLength = len(self.gradeController.listGrades())
    #     self.studentController.removeStudent('1')
    #     self.assertNotEqual(len(self.gradeController.listGrades()), gradeLength)
    #
    # def testFindStudent(self):
    #     student = self.studentController.addStudent(1, 'Ricky', 7)
    #     studentId = student.getStudentId()
    #     self.assertTrue(self.studentController.findStudent(studentId).getName() == 'Ricky')
    #     self.assertTrue(self.studentController.findStudent(studentId).getGroup() == 7)
    #     with self.assertRaises(StudentIdNotFound):
    #         self.studentController.findStudent(-1)
    #
    # def testUpdateStudent(self):
    #     student = self.studentController.addStudent(0, 'Ricky', 7)
    #     studentId = student.getStudentId()
    #     self.studentController.updateStudent(studentId, 'Andy', 11)
    #     self.assertTrue(self.studentController.findStudent(studentId).getName() == 'Andy')
    #     self.assertTrue(self.studentController.findStudent(studentId).getGroup() == 11)
    #
    # def testListStudentGrades(self):
    #     student1 = self.studentController.addStudent('Ricky', '7')
    #     student1Id = student1.getStudentId()
    #     assignment1 = self.assignmentController.addAssignment('Project1', TypeParser.parseDate('2.10.2018', ValueError))
    #     assignment1Id = assignment1.getAssignmentId()
    #     grade1 = self.gradeController.assignToStudent(student1Id, assignment1Id)
    #     assignment2 = self.assignmentController.addAssignment('Project2', '3.10.2018')
    #     assignment2Id = assignment2.getAssignmentId()
    #     grade2 = self.gradeController.assignToStudent(student1Id, assignment2Id)
    #     gradeList = self.gradeController.listStudentGrades(student1Id)
    #     self.assertTrue(grade1 in gradeList)
    #     self.assertTrue(grade2 in gradeList)
    #
    # def testAddAssignment(self):
    #     assignment = self.assignmentController.addAssignment(1, 'Project', TypeParser.parseDate('2.10.2018', ValueError))
    #     self.assertTrue(assignment.getDescription() == 'Project')
    #     self.assertTrue(assignment.getDeadline() == date(2018, 10, 2))
    #     with self.assertRaises(InvalidAssignmentDeadline):
    #         self.assignmentController.addAssignment(1, 'Project', "-9")
    #
    # def testParseDate(self):
    #     self.assertTrue(TypeParser.parseDate('2.10.2018', TypeError) == date(2018, 10, 2))
    #     with self.assertRaises(TypeError):
    #         TypeParser.parseDate('8', TypeError)
    #     with self.assertRaises(TypeError):
    #         TypeParser.parseDate('8.-7.432', TypeError)
    #
    # def testRemoveAssignment(self):
    #     oldLength = len(self.assignmentController.listAssignments())
    #     assignment = self.assignmentController.addAssignment(1, 'Project', TypeParser.parseDate('2.10.2018', ValueError))
    #     self.assignmentController.removeAssignment(str(assignment.getAssignmentId()))
    #     self.assertTrue(len(self.assignmentController.listAssignments()) == oldLength)
    #
    #     self.populateRepository()
    #     gradeLength = len(self.gradeController.listGrades())
    #     self.assignmentController.removeAssignment('1')
    #     self.assertNotEqual(len(self.gradeController.listGrades()), gradeLength)
    #
    # def testFindAssignment(self):
    #     assignment = self.assignmentController.addAssignment(1, 'Project', TypeParser.parseDate('2.10.2018', ValueError))
    #     assignmentId = assignment.getAssignmentId()
    #     self.assertTrue(self.assignmentController.findAssignment(assignmentId).getDescription() == 'Project')
    #     self.assertTrue(self.assignmentController.findAssignment(assignmentId).getDeadline() == date(2018, 10, 2))
    #     with self.assertRaises(AssignmentIdNotFound):
    #         self.assignmentController.findAssignment('-1')
    #
    # def testUpdateAssignment(self):
    #     assignment = self.assignmentController.addAssignment(1, 'Project', TypeParser.parseDate('2.10.2018', ValueError))
    #     assignmentId = assignment.getAssignmentId()
    #     self.assignmentController.updateAssignment(assignmentId, 'Project 2', '2.11.2018')
    #     self.assertTrue(self.assignmentController.findAssignment(assignmentId).getDescription() == 'Project 2')
    #     self.assertTrue(self.assignmentController.findAssignment(assignmentId).getDeadline() == date(2018, 11, 2))
    #
    # def testListAssignmentGrades(self):
    #     student1 = self.studentController.addStudent('Ricky', '7')
    #     student1Id = student1.getStudentId()
    #     student2 = self.studentController.addStudent('Michael', '8')
    #     student2Id = student2.getStudentId()
    #     assignment1 = self.assignmentController.addAssignment('Project1', TypeParser.parseDate('2.10.2018', ValueError))
    #     assignment1Id = assignment1.getAssignmentId()
    #     grade1 = self.gradeController.assignToStudent(student1Id, assignment1Id)
    #     grade2 = self.gradeController.assignToStudent(student2Id, assignment1Id)
    #     gradeList = self.gradeController.listAssignmentGrades(assignment1Id)
    #     self.assertTrue(grade1 in gradeList)
    #     self.assertTrue(grade2 in gradeList)
    #
    # def testAssignToStudent(self):
    #     student = self.studentController.addStudent(1, 'Ricky', 7)
    #     assignment = self.assignmentController.addAssignment(1, 'Project', TypeParser.parseDate('2.10.2018', ValueError))
    #     self.assertTrue(len(self.gradeController.listStudentGrades(student.getStudentId())) == 0)
    #     self.assertTrue(len(self.gradeController.listAssignmentGrades(assignment.getAssignmentId())) == 0)
    #     self.gradeController.assignToStudent(student.getStudentId(), assignment.getAssignmentId())
    #     self.assertTrue(len(self.gradeController.listStudentGrades(student.getStudentId())) == 1)
    #     self.assertTrue(len(self.gradeController.listAssignmentGrades(assignment.getAssignmentId())) == 1)
    #     self.assertTrue(self.gradeController.getGrade(student.getStudentId(), assignment.getAssignmentId())
    #                     is not None)
    #
    # def testCheckGroupExistence(self):
    #     group = 0
    #     # while group in [student.getGroup() for student in self.repository.getStudents()]:
    #     #     group += 1
    #     self.studentController.addStudent(1, 'Ricky', group)
    #     self.gradeController.checkGroupExistence(group)
    #     while group in [student.getGroup() for student in self.studentController.listStudents()]:
    #         group += 1
    #     with self.assertRaises(GroupNotFound):
    #         self.gradeController.checkGroupExistence(group)
    #
    # def testAssignToGroup(self):
    #     group = 0
    #     # while group in [student.getGroup() for student in self.repository.getStudents()]:
    #     #     group += 1
    #     student1 = self.studentController.addStudent(1, 'Ricky', group)
    #     student2 = self.studentController.addStudent(2, 'Alfred', group)
    #     student3 = self.studentController.addStudent(3, 'Alex', group)
    #     assignment = self.assignmentController.addAssignment(1, 'Project', TypeParser.parseDate('2.10.2018', ValueError))
    #     self.gradeController.assignToStudent(student1.getStudentId(), assignment.getAssignmentId())
    #     self.gradeController.assignToGroup(group, assignment.getAssignmentId())
    #     self.assertTrue(
    #         self.gradeController.getGrade(student1.getStudentId(), assignment.getAssignmentId()) is not None)
    #     self.assertTrue(
    #         self.gradeController.getGrade(student2.getStudentId(), assignment.getAssignmentId()) is not None)
    #     self.assertTrue(
    #         self.gradeController.getGrade(student3.getStudentId(), assignment.getAssignmentId()) is not None)

    # def testGrade(self):
    #     student1 = self.studentController.addStudent('Ricky', '7')
    #     student1Id = student1.getStudentId()
    #     assignment1 = self.assignmentController.addAssignment('Project1', TypeParser.parseDate('2.10.2018', ValueError))
    #     assignment1Id = assignment1.getAssignmentId()
    #     with self.assertRaises(InvalidAssignmentId):
    #         self.gradeController.grade(student1Id, assignment1Id, '1')
    #     grade = self.studentController.assignToStudent(student1Id, assignment1Id)
    #     with self.assertRaises(InvalidGrade):
    #         self.gradeController.grade(student1Id, assignment1Id, '-1')
    #     with self.assertRaises(InvalidAssignmentId):
    #         self.gradeController.grade(student1Id, '-1', '1')
    #     self.gradeController.grade(student1Id, assignment1Id, '10')
    #     self.assertEqual(grade.getGrade(), 10)
    #     with self.assertRaises(InvalidAssignmentId):
    #         self.gradeController.grade(student1Id, assignment1Id, '1')
    #
    # def testGetStudentUngradedAssignments(self):
    #     student1 = self.studentController.addStudent('Ricky', 7)
    #     student1Id = student1.getStudentId()
    #     assignment1 = self.assignmentController.addAssignment('Project1', TypeParser.parseDate('2.10.2018', ValueError))
    #     assignment1Id = assignment1.getAssignmentId()
    #     assignment2 = self.assignmentController.addAssignment('Project2', '3.10.2018')
    #     assignment2Id = assignment2.getAssignmentId()
    #     grade1 = self.gradeController.assignToStudent(student1Id, assignment1Id)
    #     grade2 = self.gradeController.assignToStudent(student1Id, assignment2Id)
    #     self.gradeController.grade(student1Id, assignment1Id, '7')
    #     assignmentList = self.gradeController.getStudentUngradedAssignments(student1Id)
    #     self.assertTrue(assignment2 in assignmentList)
    #
    # def testAssignmentGradable(self):
    #     student1 = self.studentController.addStudent(1, 'Ricky', 7)
    #     student1Id = student1.getStudentId()
    #     assignment1 = self.assignmentController.addAssignment(1, 'Project1', TypeParser.parseDate('2.10.2018', ValueError))
    #     assignment1Id = assignment1.getAssignmentId()
    #     with self.assertRaises(GradeNotFound):
    #         self.gradeController.validateGrading(student1Id, assignment1Id)
    #     self.gradeController.assignToStudent(student1Id, assignment1Id)
    #     self.gradeController.validateGrading(student1Id, assignment1Id)
    #     self.gradeController.grade(student1Id, assignment1Id, 9)
    #     with self.assertRaises(GradeAlreadySet):
    #         self.gradeController.validateGrading(student1Id, assignment1Id)
    #
    # def populateRepository(self):
    #     studentList: List[Student] = [
    #         self.studentController.addStudent(0, 'Andrew', 915),
    #         self.studentController.addStudent(1, 'Richard', 915),
    #         self.studentController.addStudent(2, 'John', 917),
    #         self.studentController.addStudent(3, 'Hori', 917)
    #     ]
    #     assignmentList: List[Assignment] = [
    #         self.assignmentController.addAssignment(0, 'Assignment 01', TypeParser.parseDate("10.10.2018", ValueError)),
    #         self.assignmentController.addAssignment(1, 'Assignment 02', TypeParser.parseDate("17.10.2018", ValueError)),
    #         self.assignmentController.addAssignment(2, 'Assignment 03-04', TypeParser.parseDate("31.10.2018", ValueError)),
    #         self.assignmentController.addAssignment(3, 'Assignment 05-07', TypeParser.parseDate("28.11.2018", ValueError))
    #     ]
    #
    #     self.gradeController.assignToStudent(studentList[0].getStudentId(),
    #                                          assignmentList[1].getAssignmentId()).setGrade(10)
    #     self.gradeController.assignToStudent(studentList[0].getStudentId(), assignmentList[3].getAssignmentId())
    #     self.gradeController.assignToStudent(studentList[1].getStudentId(),
    #                                          assignmentList[1].getAssignmentId()).setGrade(5)
    #     self.gradeController.assignToStudent(studentList[1].getStudentId(),
    #                                          assignmentList[2].getAssignmentId()).setGrade(4)
    #     self.gradeController.assignToStudent(studentList[2].getStudentId(), assignmentList[2].getAssignmentId())
    #     self.gradeController.assignToStudent(studentList[2].getStudentId(),
    #                                          assignmentList[3].getAssignmentId()).setGrade(9)
    #     self.gradeController.assignToStudent(studentList[3].getStudentId(), assignmentList[1].getAssignmentId())
    #     self.controllerWrapper.clearHistory()
    #
    # def testGetStudentsForAssignmentSortedAlphabetically(self):
    #     self.populateRepository()
    #     student = self.gradeController.findStudent
    #     output = [student(0), student(3), student(1)]
    #     self.assertEqual(output, self.gradeController.getStudentsForAssignmentSortedAlphabetically('1'))
    #
    # def testGetStudentsForAssignmentSortedByGrade(self):
    #     self.populateRepository()
    #     student = self.studentController.findStudent
    #     output = [student(0), student(1), student(3)]
    #     self.assertEqual(output, self.gradeController.getStudentsForAssignmentSortedByGrade('1'))
    #
    # def testGetStudentsSortedByAverage(self):
    #     self.populateRepository()
    #     student = self.studentController.findStudent
    #     output = [(student(0), 10), (student(2), 9), (student(1), 4.5), (student(3), 0)]
    #     self.assertEqual(output, self.gradeController.getStudentsSortedByAverage())
    #
    # def testGetAssignmentsSortedByAverage(self):
    #     self.populateRepository()
    #     assignment = self.assignmentController.findAssignment
    #     output = [(assignment(3), 9), (assignment(1), 7.5), (assignment(2), 4)]
    #     self.assertEqual(output, self.gradeController.getAssignmentsSortedByAverage())
    #
    # def testGetGrade(self):
    #     student1 = self.studentController.addStudent('Ricky', '7')
    #     student1Id = student1.getStudentId()
    #     assignment1 = self.assignmentController.addAssignment('Project1', TypeParser.parseDate('2.10.2018', ValueError))
    #     assignment1Id = assignment1.getAssignmentId()
    #     grade = self.gradeController.assignToStudent(student1Id, assignment1Id)
    #     self.assertEqual(grade, self.gradeController.getGrade(student1Id, assignment1Id))
    #
    # def testLateStudents(self):
    #     self.populateRepository()
    #     student = self.studentController.findStudent
    #     output = [student(2), student(3)]
    #     self.assertEqual(output, self.gradeController.lateStudents())
    #
    # def testUndoRedo(self):
    #     self.populateRepository()
    #
    #     studentNumber = len(self.studentController.listStudents())
    #     self.studentController.addStudent("Sample Name", '67')
    #     self.assertEqual(len(self.studentController.listStudents()), studentNumber + 1)
    #     self.controllerWrapper.undo()
    #     self.assertEqual(len(self.studentController.listStudents()), studentNumber)
    #     self.controllerWrapper.undo()
    #     self.assertEqual(len(self.studentController.listStudents()), studentNumber)
    #     self.controllerWrapper.redo()
    #     self.assertEqual(len(self.studentController.listStudents()), studentNumber + 1)
    #     self.controllerWrapper.redo()
    #     self.assertEqual(len(self.studentController.listStudents()), studentNumber + 1)
    #     self.controllerWrapper.clearHistory()
    #
    #     gradeNumber = len(self.gradeController.listGrades())
    #     self.gradeController.assignToStudent('1', '0')
    #     self.assertEqual(len(self.gradeController.listGrades()), gradeNumber + 1)
    #     self.controllerWrapper.undo()
    #     self.assertEqual(len(self.gradeController.listGrades()), gradeNumber)
    #     self.controllerWrapper.undo()
    #     self.assertEqual(len(self.gradeController.listGrades()), gradeNumber)
    #     self.controllerWrapper.redo()
    #     self.assertEqual(len(self.gradeController.listGrades()), gradeNumber + 1)
    #     self.controllerWrapper.redo()
    #     self.assertEqual(len(self.gradeController.listGrades()), gradeNumber + 1)
    #     self.controllerWrapper.clearHistory()
    #
    #     assignmentNumber = len(self.assignmentController.listAssignments())
    #     self.assignmentController.addAssignment("Sample description", '6.7.2018')
    #     self.assertEqual(len(self.assignmentController.listAssignments()), assignmentNumber + 1)
    #     self.controllerWrapper.undo()
    #     self.assertEqual(len(self.assignmentController.listAssignments()), assignmentNumber)
    #     self.controllerWrapper.undo()
    #     self.assertEqual(len(self.assignmentController.listAssignments()), assignmentNumber)
    #     self.controllerWrapper.redo()
    #     self.assertEqual(len(self.assignmentController.listAssignments()), assignmentNumber + 1)
    #     self.controllerWrapper.redo()
    #     self.assertEqual(len(self.assignmentController.listAssignments()), assignmentNumber + 1)
    #     self.controllerWrapper.clearHistory()
    #
    # def testChangesHandlerAbstract(self):
    #     ChangesHandler().handleChanges([], True)
