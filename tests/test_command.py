from datetime import timedelta
from fox_sdk.command import FAMOVE, FARESULT, FASKIP, FATIMELEFT, AFCommands, Move, Player, FASTATUS, encode, load_command, get_checksum, load_commands, verify_checksum


def hydrate(data: str):
    cksum = get_checksum(data)
    return '${}*{}\r\n'.format(data, cksum)


def test_get_checksum():
    cksum = get_checksum('FASTATUS,0')
    assert cksum == '0F'


def test_verify_checksum():
    assert verify_checksum('$FASTATUS,0*0F\r\n')
    assert not verify_checksum('$FASTATUS,0*0E\r\n', raise_exception=False)


def test_load_status():
    command: FASTATUS = load_command(
        hydrate('FASTATUS,1,W,1^12^11^B'))
    assert command.is_playing

    moves = list(command.moves)
    assert isinstance(command, FASTATUS)
    assert len(moves) == 1
    [move] = moves
    assert move.step == 1
    assert move.player == Player.BLACK
    assert move.x == 12
    assert move.y == 11


def test_encode():
    encoded = encode('AFSTATUS')
    assert encoded == b'$AFSTATUS*13\r\n'


def test_not_playing():
    command = load_command('$FASTATUS,0*0F\r\n')

    assert isinstance(command, FASTATUS)
    assert command.command == 'FASTATUS'
    assert command.content == '0'
    assert command.data == ['0']


def test_move():
    command = load_command("$FAMOVE,1,B,2^3^2^W*73\r\n")
    assert isinstance(command, FAMOVE)
    assert command.AI_player == Player.BLACK

    assert command.is_AI
    assert command.move == Move(step=2, player=Player.WHITE, x=3, y=2)


def test_rule():
    command = load_command("$FARULE,19,1200,30,3,650,1^3^2^B*2D\r\n")
    assert command.size == 19
    assert command.duration == timedelta(seconds=1200)
    assert command.byo_yomi_duration == timedelta(seconds=30)
    assert command.byo_yomi_count == 3
    assert command.komi == 6.5
    assert list(command.handicap_moves) == [Move(step=1, x=3, y=2, player=Player.BLACK)]


def test_result():
    command = load_command('$FARESULT,W+550*6E\r\n')
    assert isinstance(command, FARESULT)
    assert command.winner == Player.WHITE
    assert command.score == 5.5


def test_timeleft():
    command = load_command('$FATIMELEFT,1196,30,3*1A\r\n')
    assert isinstance(command, FATIMELEFT)
    assert command.duration == timedelta(seconds=1196)
    assert command.byo_yomi_duration == timedelta(seconds=30)
    assert command.byo_yomi_count == 3


def test_skip():
    command = load_command('$FASKIP,0,W*00\r\n')
    assert isinstance(command, FASKIP)
    assert not command.is_AI
    assert command.AI_player == Player.WHITE


def test_af_play():
    command = AFCommands.play(Player.BLACK, Move(step=1, x=12, y=11, player=Player.BLACK))
    assert command == b'$AFPLAY,B,1^12^11^B*6F\r\n'


def test_af_skip():
    command = AFCommands.skip(Player.WHITE)
    assert command == b'$AFSKIP,W*7D\r\n'


def test_af_give_up():
    command = AFCommands.give_up(Player.WHITE)
    assert command == b'$AFGIVEUP,W*64\r\n'


def test_load_commands():
    str1 = '$FASKIP,0,W*00\r\n'
    str2 = '$FATIMELEFT,1196,30,3*1A\r\n'
    commands1 = list(load_commands(str1 + str2))

    commands2 = [load_command(str1), load_command(str2)]

    assert commands1 == commands2
