from enum import Enum, unique


@unique
class Gender(Enum):

    MALE = 'М'
    FEMALE = 'Ж'
    NEW = 'Н'
    EXPERT = 'Э'
