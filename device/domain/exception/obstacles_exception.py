from .domain_exception import DomainException


class ObstaclesDetectorException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)
