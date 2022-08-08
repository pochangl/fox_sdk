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
