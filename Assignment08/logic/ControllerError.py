class ControllerError(Exception):
    pass


class GroupNotFound(ControllerError):
    pass


class AssignmentIdNotFound(ControllerError):
    pass


class StudentIdNotFound(ControllerError):
    pass


class GradeNotFound(ControllerError):
    pass


class GradeAlreadySet(ControllerError):
    pass
