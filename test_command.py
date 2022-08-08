from command import FoxToAICommand, load_command, get_checksum, verify_checksum


def test_get_checksum():
    cksum = get_checksum('FASTATUS,0')
    assert cksum == '0F'


def test_verify_checksum():
    assert verify_checksum('$FASTATUS,0*0F\r\n')
    assert not verify_checksum('$FASTATUS,0*0E\r\n')


def test_load_command():
    command = load_command('$FASTATUS,0*0F\r\n')

    assert isinstance(command, FoxToAICommand)
    assert command.command == 'FASTATUS'
    assert command.content == '0'
    assert command.data == ['0']
