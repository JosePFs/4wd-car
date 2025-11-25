from .domain_exception import DomainException


class CommandException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidCommandException(CommandException):
    def __init__(self, message: str):
        super().__init__(message)
