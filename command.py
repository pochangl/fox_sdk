from dataclasses import dataclass
from datetime import timedelta
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


class FACommands(Enum):
    STATUS = 'FASTATUS'
    MOVE = 'FAMOVE'
    SKIP = 'FASKIP'
    RESULT = 'FARESULT'
    RULE = 'FARULE'
    TIME_LEFT = 'FATIMELEFT'
    SCORE = 'FASCORE'


class AFCommands(Enum):
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
class FACommand(Command):
    command: FACommands
    data: 'list[str]'


@dataclass
class Move:
    step: int
    x: int
    y: int
    player: Player

    @staticmethod
    def from_str(string: str) -> 'Move':
        index, x, y, color = string.split('^')
        return Move(int(index), int(x), int(y), Player.from_color(color))


class FASTATUS(FACommand):
    @property
    def is_playing(self):
        return self.data[0] == '1'

    @property
    def color(self) -> Player:
        return Player.from_color(self.data[0])

    @property
    def moves(self) -> 'Iterable[Move]':
        yield from map(Move.from_str, self.data[2:])


class FAMOVE(FACommand):
    @property
    def is_AI(self) -> bool:
        return self.data[0] == '1'

    @property
    def AI_player(self) -> Player:
        return Player.from_color(self.data[1])

    @property
    def move(self) -> Move:
        return Move.from_str(self.data[2])


class FARULE(FACommand):
    @property
    def size(self):
        return int(self.data[0])

    @property
    def duration(self):
        return timedelta(seconds=int(self.data[1]))

    @property
    def byo_yomi_duration(self):
        return timedelta(seconds=int(self.data[2]))

    @property
    def byo_yomi_count(self):
        return int(self.data[3])

    @property
    def komi(self):
        return int(self.data[4]) / 100

    @property
    def handicap_moves(self):
        yield from map(Move.from_str, self.data[5:])


commands = {
    FACommands.STATUS.value: FASTATUS,
    FACommands.MOVE.value: FAMOVE,
    FACommands.RULE.value: FARULE,
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
        return FACommand(
            command=command,
            content=content,
            data=content.split(','),
        )
