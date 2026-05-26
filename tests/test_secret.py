import unittest.mock

import pytest
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


@unittest.mock.patch.dict(
    'os.environ',
    {'HOVERPOWER_SECRET': 'newvalue'},  # nosec
)
def test_decode_invalid_format():
    """Fail if secret is not 32 bytes long."""
    completed = utilo.run(
        'powerdecrypt',
        expect=False,
    )
    assert '[ERROR] Invalid HOVERPOWER_SECRET format: newvalue' in completed.stderr

@pytest.mark.xfail(reason='prepare implemtation')
@unittest.mock.patch.dict(
    'os.environ',
    {'HOVERPOWER_SECRET': hoverpower.secret.DEFAULT_SECRET.decode()},  # nosec
)
def test_decode_invalid_secret():
    """Stop extracting resources after first invalid secret."""
    completed = utilo.run(
        'powerdecrypt',
        expect=False,
    )
    error = completed.stderr
    count = error.count('[ERROR] invalid HOVERPOWER_SECRET')
    assert count == 1
