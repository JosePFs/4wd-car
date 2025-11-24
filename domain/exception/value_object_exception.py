from .domain_exception import DomainException


class ValueObjectException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidValueException(ValueObjectException):
    def __init__(self, message: str):
        super().__init__(message)
