from dataclasses import dataclass
from enum import Enum
import re
from typing import Iterable


class Player(Enum):
    BLACK = 'B'
    WHITE = 'W'

    @classmethod
    def from_color(cls, color: str):
        if color == Player.BLACK.value:
            return Player.BLACK
        elif color == Player.WHITE.value:
            return Player.WHITE
        else:
            raise Exception('unknown color {}'.format(color))


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


def encode(data: str):
    checksum = get_checksum(data)
    return '${}*{}\r\n'.format(data, checksum).encode()


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


@dataclass
class Move:
    index: int
    x: int
    y: int
    player: Player


class StatusCommand(FoxToAICommand):
    @property
    def is_playing(self):
        return self.data[0] == '1'

    @property
    def color(self) -> Player:
        if self.data[0] == Player.BLACK:
            return Player.BLACK
        else:
            return Player.WHITE

    @property
    def moves(self) -> 'Iterable[Move]':
        for move in self.data[2:]:
            index, x, y, color = move.split('^')
            yield Move(int(index), int(x), int(y), Player.from_color(color))


commands = {
    FoxToAICommands.STATUS.value: StatusCommand
}


def load_command(data: str):
    assert isinstance(data, str), 'must be str instance'
    assert verify_checksum(data), 'invalid checksum'
    m = re.search(r'^\$(.+)\*([0-9A-F]{2})\r\n$', data)

    text = m.group(1)
    command, content = text.split(',', 1)

    if command in commands:
        return commands[command](
            command=command,
            content=content,
            data=content.split(','),
        )
    else:
        return FoxToAICommand(
            command=command,
            content=content,
            data=content.split(','),
        )
