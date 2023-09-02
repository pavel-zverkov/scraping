from enum import Enum, unique


@unique
class Qualify(Enum):

    MSMK = 'МСМК'
    ZMS = 'ЗМС'
    MS = 'МС'
    KMS = 'КМС'
    I = 'I'
    II = 'II'
    III = 'III'
    Iun = 'Iюн'
    IIun = 'IIюн'
    IIIun = 'IIIюн'
