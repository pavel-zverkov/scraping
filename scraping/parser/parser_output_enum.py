from enum import Enum, unique


@unique
class OutputStatus(Enum):
    SUCCESS: 0
    ERROR: 1