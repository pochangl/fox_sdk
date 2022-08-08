from command import get_checksum


def test_get_checksum():
    cksum = get_checksum('FASTATUS,0')
    assert cksum == '0F'
