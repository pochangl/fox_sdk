from command import FAMOVE, FACommand, Move, Player, FASTATUS, encode, load_command, get_checksum, verify_checksum


def hydrate(data: str):
    cksum = get_checksum(data)
    return '${}*{}\r\n'.format(data, cksum)


def test_get_checksum():
    cksum = get_checksum('FASTATUS,0')
    assert cksum == '0F'


def test_verify_checksum():
    assert verify_checksum('$FASTATUS,0*0F\r\n')
    assert not verify_checksum('$FASTATUS,0*0E\r\n')


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

    assert command.is_AI == True
    assert command.move == Move(step=2, player=Player.WHITE, x=3, y=2)
