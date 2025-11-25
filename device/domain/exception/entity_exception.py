from .domain_exception import DomainException


class EntityException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)


class EntityIdException(EntityException):
    def __init__(self, message: str):
        super().__init__(message)
