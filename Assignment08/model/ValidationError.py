class ValidationError(RuntimeError):
    pass


class InvalidStudentId(ValidationError):
    pass


class InvalidStudentName(ValidationError):
    pass


class InvalidStudentGroup(ValidationError):
    pass


class InvalidAssignmentId(ValidationError):
    pass


class InvalidAssignmentDescription(ValidationError):
    pass


class InvalidAssignmentDeadline(ValidationError):
    pass


class InvalidGrade(ValidationError):
    pass
