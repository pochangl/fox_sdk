from enum import Enum


class FoxToAICommand(Enum):
    STATUS = '$FASTATUS'
    MOVE = '$FAMOVE'
    SKIP = '$FASKIP'
    RESULT = '$FARESULT'
    RULE = '$FARULE'
    TIME_LEFT = '$FATIMELEFT'
    SCORE = '$FASCORE'


class AIToFoxCommand(Enum):
    PLAY = '$AFPLAY'
    STATUS = '$AFSTATUS'
    SKIP = '$AFSKIP'
    GIVE_UP = '$AFGIVEUP'
    SCORE = '$AFSCORE'


def get_checksum(data: str):
    sum = 0
    for byte in data:
        print(byte, ord(byte))
        sum ^= ord(byte)
    return hex(sum)[2:].upper().zfill(2)
