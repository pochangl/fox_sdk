from dataclasses import dataclass
from enum import Enum
import re


class FoxToAICommands(Enum):
    STATUS = 'FASTATUS'
    MOVE = 'FAMOVE'
    SKIP = 'FASKIP'
    RESULT = 'FARESULT'
    RULE = 'FARULE'
    TIME_LEFT = 'FATIMELEFT'
    SCORE = 'FASCORE'


class AIToFoxCommands(Enum):
    PLAY = 'AFPLAY'
    STATUS = 'AFSTATUS'
    SKIP = 'AFSKIP'
    GIVE_UP = 'AFGIVEUP'
    SCORE = 'AFSCORE'


def get_checksum(data: str):
    assert isinstance(data, str), 'must be str instance'
    sum = 0
    for byte in data:
        sum ^= ord(byte)
    return hex(sum)[2:].upper().zfill(2)


def verify_checksum(data: str):
    assert isinstance(data, str), 'must be str instance'
    m = re.search(r'^\$(.+)\*([0-9A-F]{2})\r\n$', data)

    checksum1 = get_checksum(m.group(1))
    checksum2 = m.group(2)
    return checksum1 == checksum2


@dataclass
class Command:
    command: str
    content: str


@dataclass
class FoxToAICommand(Command):
    command: FoxToAICommands
    data: 'list[str]'


def load_command(data: str):
    assert isinstance(data, str), 'must be str instance'
    assert verify_checksum(data), 'invalid checksum'
    m = re.search(r'^\$(.+)\*([0-9A-F]{2})\r\n$', data)

    text = m.group(1)
    command, content = text.split(',', 1)

    return FoxToAICommand(command=command, content=content, data=content.split(','))
