from .domain_exception import DomainException


class CarException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)

class AutonomousPilotException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)