from enum import Enum
from dataclasses import dataclass
import logging


class Mode(Enum):
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
    TEST = 'test'


@dataclass
class ApplicationConfig:
    mode: Mode = Mode.DEVELOPMENT
    log_level: int = logging.INFO

    @classmethod
    def development(cls) -> 'ApplicationConfig':
        return cls(mode=Mode.DEVELOPMENT, log_level=logging.DEBUG)

    @classmethod
    def production(cls) -> 'ApplicationConfig':
        return cls(mode=Mode.PRODUCTION, log_level=logging.INFO)

    @classmethod
    def test(cls) -> 'ApplicationConfig':
        return cls(mode=Mode.TEST, log_level=logging.DEBUG)
