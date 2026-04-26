import utilo

import hoverpower.secret

SOURCE = 'secret.txt'
DEST = 'encrypted.bin'
DATA = b'line1'


def test_encode_decode(testdir):
    utilo.file_create_binary(SOURCE, DATA)
    encrypted = hoverpower.secret.encrypt(SOURCE)
    utilo.file_create_binary(DEST, encrypted)
    decrypted = hoverpower.secret.decrypt(DEST)
    assert decrypted == DATA
