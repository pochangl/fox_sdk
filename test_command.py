from command import get_checksum, verify_checksum


def test_get_checksum():
    cksum = get_checksum('FASTATUS,0')
    assert cksum == '0F'


def test_verify_checksum():
    assert verify_checksum('$FASTATUS,0*0F\r\n')
    assert not verify_checksum('$FASTATUS,0*0E\r\n')
