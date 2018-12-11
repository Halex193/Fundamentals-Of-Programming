from datetime import date
from tkinter import *
from tkinter import messagebox

from logic.ControllerError import *
from logic.ControllerWrapper import ControllerWrapper
from model.Assignment import Assignment
from model.Grade import Grade
from model.Student import Student
from model.ValidationError import *
from repository.RepositoryError import DuplicateItemError
from ui.UI import UI
from utils.TypeParser import TypeParser


class GUI(UI):

    def __init__(self, controllerWrapper: ControllerWrapper):
        UI.__init__(self, controllerWrapper)
        self.frame1 = None
        self.frame2 = None
        self.frame3 = None
        self.frame4 = None
        self.frame5 = None
        self.frame6 = None
        self.frame7 = None
        self.studentId = None
        self.studentName = None
        self.studentGroup = None
        self.assignmentId = None
        self.assignmentDescription = None
        self.assignmentDeadline = None
        self.grade = None
        self.studentController = controllerWrapper.getStudentController()
        self.gradeController = controllerWrapper.getGradeController()
        self.assignmentController = controllerWrapper.getAssignmentController()

        self.__window = self.buildWindow()

    def run(self):
        self.__window.mainloop()

    def buildWindow(self) -> Tk:
        tk = Tk()
        tk.report_callback_exception = self.handleCustomError
        tk.title("Assignment manager")

        Button(tk, text="List repository", command=self.listRepository, width=30).pack(pady=10)

        frame1 = Frame(tk)
        frame1.pack(pady=10)

        labelStudent = Label(frame1, text="Student: ")
        labelStudent.pack(side=LEFT)

        self.addEntry(frame1, "Id:", "studentId")
        self.addEntry(frame1, "Name:", "studentName")
        self.addEntry(frame1, "Group:", "studentGroup")

        frame2 = Frame(tk)
        frame2.pack(pady=10)
        self.frame2 = frame2

        Label(frame2, text="Assignment").pack(side=LEFT)

        self.addEntry(frame2, "Id:", "assignmentId")
        self.addEntry(frame2, "Description:", "assignmentDescription")
        self.addEntry(frame2, "Deadline:", "assignmentDeadline")

        frame3 = Frame(tk)
        frame3.pack(pady=10)
        self.frame3 = frame3

        self.addEntry(frame3, "Grade: ", "grade")

        frame4 = Frame(tk)
        frame4.pack(side=LEFT, pady=20, padx=20)
        self.frame4 = frame4

        Label(frame4, text="Manage Students").pack(fill=BOTH)
        self.addButton(frame4, "List students", self.listStudents)
        self.addButton(frame4, "Add student", self.addStudent)
        self.addButton(frame4, "Remove student", self.removeStudent)
        self.addButton(frame4, "Update student", self.updateStudent)
        self.addButton(frame4, "List student grades", self.listStudentGrades)

        frame5 = Frame(tk)
        frame5.pack(side=LEFT, pady=20, padx=20)
        self.frame5 = frame5

        Label(frame5, text="Manage Assignments").pack(fill=BOTH)
        self.addButton(frame5, "List assignments", self.listAssignments)
        self.addButton(frame5, "Add assignment", self.addAssignment)
        self.addButton(frame5, "Remove assignment", self.removeAssignment)
        self.addButton(frame5, "Update assignment", self.updateAssignment)
        self.addButton(frame5, "List assignment grades", self.listAssignmentGrades)

        frame6 = Frame(tk)
        frame6.pack(side=RIGHT, pady=20, padx=20)
        self.frame6 = frame6

        Label(frame6, text="Statistics").pack(fill=BOTH)
        self.addButton(frame6, "Students with specified assignment, ordered alphabetically",
                       self.studentsSortedAlphabetically, 50)
        self.addButton(frame6, "Students with specified assignment, ordered by grade", self.studentsSortedByGrade, 50)
        self.addButton(frame6, "Late students", self.lateStudents, 50)
        self.addButton(frame6, "Students sorted descending by average grade", self.studentsSortedByAverage, 50)
        self.addButton(frame6, "Assignments sorted descending by average grade", self.assignmentsSortedByAverage, 50)

        frame7 = Frame(tk)
        frame7.pack(side=RIGHT, pady=20, padx=20)
        self.frame7 = frame7

        Label(frame7, text="Other operations").pack(fill=BOTH)
        self.addButton(frame7, "Grade student", self.gradeStudent, 30)
        self.addButton(frame7, "Give assignment to student", self.assignToStudent, 30)
        self.addButton(frame7, "Give assignment to group of students", self.assignToGroup, 30)
        self.addButton(frame7, "Undo", self.undo, 30)
        self.addButton(frame7, "Redo", self.redo, 30)
        return tk

    def addEntry(self, frame: Frame, text: str, entryName: str):
        Label(frame, text=text).pack(side=LEFT)
        self.__dict__[entryName] = Entry(frame, {})
        self.__dict__[entryName].pack(side=LEFT)

    @staticmethod
    def addButton(frame: Frame, text: str, callback: callable, width: int = 20):
        Button(frame, text=text, command=callback, width=width).pack(pady=2)

    def handleCustomError(self, *args):
        error = args[1]

        def getDuplicateItemMessage(genericError):
            if type(genericError) is not DuplicateItemError:
                return ''
            return {
                Student: "Student already exists",
                Grade: "Student was already given this assignment",
                Assignment: "Assignment already exists"
            }[error.getItemType()]

        errorTypes = {
            DuplicateItemError: getDuplicateItemMessage(error),
            InvalidStudentId: "Student id is invalid",
            InvalidStudentGroup: "Student group is invalid",
            InvalidAssignmentId: "Assignment id is invalid",
            InvalidAssignmentDeadline: "Assignment deadline is invalid",
            InvalidGrade: "Grade must be an integer between 0 and 10",
            GroupNotFound: "There is no student with the given group",
            AssignmentIdNotFound: "There is no assignment with the given id",
            StudentIdNotFound: "There is no student with the given id",
            GradeNotFound: "Student was not given the specified assignment",
            GradeAlreadySet: "The student was already graded for the assignment"

        }
        if type(error) in errorTypes:
            messagebox.showerror("Error", errorTypes[type(error)])
        else:
            raise error

    def listStudents(self):
        studentList = self.studentController.listStudents()
        output = ["\nID - Name - Group\n"]
        for student in studentList:
            output.append(self.studentToStr(student) + '\n')
        messagebox.showinfo("Student list", ''.join(output))

    @staticmethod
    def studentToStr(student: Student):
        return str(student.getStudentId()) + " - " + student.getName() + " - " + str(student.getGroup())

    def addStudent(self):
        studentId = self.studentId.get()
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        name = self.studentName.get()
        group = self.studentGroup.get()
        group = TypeParser.parseInt(group, InvalidStudentGroup)
        self.studentController.addStudent(studentId, name, group)
        messagebox.showinfo("Info", "Student added")

    def removeStudent(self):
        studentId = self.studentId.get()
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        self.studentController.removeStudent(studentId)
        messagebox.showinfo("Info", "Student removed")

    def updateStudent(self):
        studentId = self.studentId.get()
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        student = self.studentController.findStudent(studentId)
        # print("You are modifying the student with name " + student.getName() + " from group " + str(
        #     student.getGroup()))
        name = self.studentName.get()
        group = self.studentGroup.get()
        group = TypeParser.parseInt(group, InvalidStudentGroup)
        self.studentController.updateStudent(studentId, name, group)
        messagebox.showinfo("Info", "Student information updated")

    def listStudentGrades(self):
        studentId = self.studentId.get()
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        student = self.studentController.findStudent(studentId)
        gradeList = self.controllerWrapper.getGradeController().listStudentGrades(studentId)
        if len(gradeList) == 0:
            messagebox.showinfo("Info", "No grades to show")
        else:
            output = [student.getName() + "'s grades are:\n", "Grade - Assignment ID\n"]
            for grade in gradeList:
                output.append(self.gradeToStr(grade) + '\n')
            messagebox.showinfo("Student grades", ''.join(output))

    @staticmethod
    def gradeToStr(grade) -> str:
        return str(grade.getGrade()) if grade.getGrade() is not None else "No grade"

    @staticmethod
    def studentGradeToStr(grade):
        gradeString = GUI.gradeToStr(grade)
        return gradeString + " - " + str(grade.getAssignmentId())

    def listAssignments(self):
        assignmentList = self.assignmentController.listAssignments()
        output = ["\nID - Description - Deadline\n"]
        for assignment in assignmentList:
            output.append(self.assignmentToStr(assignment) + '\n')
        messagebox.showinfo("Info", ''.join(output))

    def addAssignment(self):
        assignmentId = self.assignmentId.get()
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        description = self.assignmentDescription.get()
        deadline = self.assignmentDeadline.get()
        deadline = TypeParser.parseDate(deadline, InvalidAssignmentDeadline)
        self.assignmentController.addAssignment(assignmentId, description, deadline)
        messagebox.showinfo("Info", "Assignment added")

    def removeAssignment(self):
        assignmentId = self.assignmentId.get()
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        self.assignmentController.removeAssignment(assignmentId)
        messagebox.showinfo("Info", "Assignment removed")

    def updateAssignment(self):
        assignmentId = self.assignmentId.get()
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.assignmentController.findAssignment(assignmentId)
        # print(
        #     "You are modifying the assignment with description '" + assignment.getDescription() +
        #     "' and deadline " + GUI.dateToStr(assignment.getDeadline()))
        description = self.assignmentDescription.get()
        deadline = self.assignmentDeadline.get()
        deadline = TypeParser.parseDate(deadline, InvalidAssignmentDeadline)
        self.assignmentController.updateAssignment(assignmentId, description, deadline)
        messagebox.showinfo("Info", "Assignment information updated")

    @staticmethod
    def assignmentToStr(assignment: Assignment):
        deadline = GUI.dateToStr(assignment.getDeadline())
        return str(
            assignment.getAssignmentId()) + " - " + assignment.getDescription() + " - " + deadline

    @staticmethod
    def dateToStr(parameterDate: date):
        return str(parameterDate.day) + "." + str(parameterDate.month) + "." + str(parameterDate.year)

    def listAssignmentGrades(self):
        assignmentId = self.assignmentId.get()
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.assignmentController.findAssignment(assignmentId)
        gradeList = self.controllerWrapper.getGradeController().listAssignmentGrades(assignmentId)
        if len(gradeList) == 0:
            messagebox.showinfo("Info", "No grades to show")
        else:
            output = ["List of grades for the assignment with description '" + assignment.getDescription() + "':\n",
                      "\nGrade - Student ID\n"]
            for grade in gradeList:
                output.append(self.gradeToStr(grade) + '\n')
            messagebox.showinfo("List of grades", ''.join(output))

    @staticmethod
    def assignmentGradeToStr(grade):
        gradeString = GUI.gradeToStr(grade)
        return gradeString + " - " + str(grade.getStudentId())

    def gradeStudent(self):
        gradeController = self.controllerWrapper.getGradeController()
        studentId = self.studentId.get()
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        student = gradeController.findStudent(studentId)
        # print("You are grading the student with name " + student.getName() + " from group " + str(
        #     student.getGroup()))
        assignmentList = gradeController.getStudentUngradedAssignments(studentId)
        if len(assignmentList) == 0:
            messagebox.showinfo("Info", "The student has no ungraded assignments")
            return
        assignmentId = self.assignmentId.get()

        try:
            assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
            assignment = gradeController.findAssignment(assignmentId)
            gradeController.validateGrading(studentId, assignmentId)
        except Exception:
            output = ["\nID - Description - Deadline\n"]
            for assignment in assignmentList:
                output.append(GUI.assignmentToStr(assignment) + '\n')
            messagebox.showinfo("Ungraded assignments", ''.join(output))
            return

        # print(
        #     "You are grading the assignment with description '" + assignment.getDescription() +
        #     "' and deadline " + GUI.dateToStr(assignment.getDeadline()))
        grade = self.grade.get()
        grade = TypeParser.parseInt(grade, InvalidGrade)
        gradeController.grade(studentId, assignmentId, grade)
        messagebox.showinfo("Info", "Assignment was graded")

    def undo(self):
        if self.controllerWrapper.undo():
            messagebox.showinfo("Info", "Last operation undone")
        else:
            messagebox.showerror("Error", "No operation left to undo")

    def redo(self):
        if self.controllerWrapper.redo():
            messagebox.showinfo("Info", "Last undo operation reversed")
        else:
            messagebox.showerror("Error", "No undo operation left to reverse")

    def listRepository(self):
        self.listStudents()
        output = ["\nStudentId - AssignmentId - Grade\n"]
        for grade in self.controllerWrapper.getGradeController().listGrades():
            output.append(str(grade) + '\n')
        messagebox.showinfo("Grade list", ''.join(output))
        self.listAssignments()

    def assignToStudent(self):
        studentId = self.studentId.get()
        studentId = TypeParser.parseInt(studentId, InvalidStudentId)
        student = self.gradeController.findStudent(studentId)
        # print("You giving an assignment to the student with name " + student.getName() + " from group " + str(
        #     student.getGroup()))
        assignmentId = self.assignmentId.get()
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.gradeController.findAssignment(assignmentId)
        # print(
        #     "You are giving the assignment with description '" + assignment.getDescription() +
        #     "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
        self.gradeController.assignToStudent(studentId, assignmentId)
        messagebox.showinfo("Info", "Assignment was given")

    def assignToGroup(self):
        group = self.studentGroup.get()
        group = TypeParser.parseInt(group, InvalidStudentGroup)
        self.gradeController.checkGroupExistence(group)
        assignmentId = self.assignmentId.get()
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.gradeController.findAssignment(assignmentId)
        # print(
        #     "You are giving the assignment with description '" + assignment.getDescription() +
        #     "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))
        self.gradeController.assignToGroup(group, assignmentId)
        messagebox.showinfo("Info", "Assignments were given")

    def studentsSortedAlphabetically(self):
        assignmentId = self.assignmentId.get()
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.gradeController.findAssignment(assignmentId)
        # print(
        #     "You are viewing the students ordered alphabetically for the assignment with "
        #     "description '" + assignment.getDescription() +
        #     "' and deadline " + ManageAssignmentsMenu.dateToStr(assignment.getDeadline()))

        studentList = self.gradeController.getStudentsForAssignmentSortedAlphabetically(assignmentId)
        if len(studentList) == 0:
            messagebox.showinfo("Info", "No students received this assignment")
            return
        output = ["\nID - Name - Group\n"]
        for student in studentList:
            output.append(self.studentToStr(student) + '\n')
        messagebox.showinfo("Student list", ''.join(output))

    def studentsSortedByGrade(self):
        assignmentId = self.assignmentId.get()
        assignmentId = TypeParser.parseInt(assignmentId, InvalidAssignmentId)
        assignment = self.gradeController.findAssignment(assignmentId)
        # print(
        #     "You are viewing the students ordered by grade for the assignment with "
        #     "description '" + assignment.getDescription() +
        #     "' and deadline " + self.dateToStr(assignment.getDeadline()))

        studentList = self.gradeController.getStudentsForAssignmentSortedByGrade(assignmentId)
        if len(studentList) == 0:
            messagebox.showinfo("Info", "No students received this assignment")
            return
        output = ["\nID - Name - Group - Grade\n"]
        for student in studentList:
            gradeObject = self.gradeController.getGrade(student.getStudentId(), assignmentId)
            output.append(self.studentToStr(student) + " - " +
                          self.gradeToStr(gradeObject) + '\n')
        messagebox.showinfo("Student list", ''.join(output))

    def studentsSortedByAverage(self):
        resultList = self.gradeController.getStudentsSortedByAverage()
        if len(resultList) == 0:
            messagebox.showinfo("Info", "No students to show")
            return
        output = ["\nID - Name - Group - Average grade\n"]
        for dto in resultList:
            averageGrade = (str(dto.getAverage()) if dto.getAverage() != 0 else "No grades")
            output.append(self.studentToStr(dto.getStudent()) + " - " + averageGrade + '\n')
        messagebox.showinfo("Info", ''.join(output))

    def assignmentsSortedByAverage(self):
        resultList = self.gradeController.getAssignmentsSortedByAverage()
        if len(resultList) == 0:
            messagebox.showinfo("Info", "No assignments to show")
            return
        output = ["\nID - Description - Deadline - Average Grade\n"]
        for dto in resultList:
            output.append(self.assignmentToStr(dto.getAssignment()) + " - " + str(dto.getAverage()) + '\n')
        messagebox.showinfo("Assignment list", ''.join(output))

    def lateStudents(self):
        studentList = self.gradeController.lateStudents()
        if len(studentList) == 0:
            messagebox.showinfo("Info", "No students are late with their assignments")
            return
        output = ["\nID - Name - Group\n"]
        for student in studentList:
            output.append(self.studentToStr(student) + '\n')
        messagebox.showinfo("Late students", ''.join(output))
