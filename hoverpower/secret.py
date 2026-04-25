# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import cryptography.fernet
import utilo

import hoverpower.path

DEFAULT_SECRET = b'ohrfFMW4YeHu96rkblrD-i4PEIsV_5jFCfZWfgkUgLk='

HOVERPOWER_SECRET = os.environ.get('HOVERPOWER_SECRET', DEFAULT_SECRET)

CIPHER = cryptography.fernet.Fernet(key=HOVERPOWER_SECRET)


def decrypt(path: str) -> bytes:
    """Read encypted file content and make it raw."""
    encrypted = utilo.file_read_binary(path)
    data = CIPHER.decrypt(encrypted)
    return data


def encrypt(path: str) -> bytes:
    """Read raw file content and make it secure."""
    data = utilo.file_read_binary(path)
    encrypted = CIPHER.encrypt(data)
    return encrypted


def create_secret():
    key = cryptography.fernet.Fernet.generate_key()
    print(key)


def make_private():
    for item in hoverpower.path.RESOURCES:
        if 'https://' in item:
            continue
        if '.pdf' not in item:
            continue
        utilo.log(item)
        encrypted = encrypt(item)
        utilo.file_replace_binary(
            path=item,
            content=encrypted,
        )


def make_public():
    for item in hoverpower.path.RESOURCES:
        if 'https://' in item:
            continue
        if '.pdf' not in item:
            continue
        utilo.log(item)
        public = decrypt(item)
        utilo.file_replace_binary(
            path=item,
            content=public,
        )


def disable_pdf_tracking():
    if not isgit():
        return
    utilo.log('disable tracking')
    cmd = 'git update-index --skip-worktree hoverpower/repo/*/*.pdf'
    utilo.run(
        cmd,
        cwd=hoverpower.path.REPO,
    )


def enable_pdf_tracking():
    if not isgit():
        return
    utilo.log('enable tracking')
    cmd = 'git update-index --no-skip-worktree hoverpower/repo/*/*.pdf'
    utilo.run(
        cmd,
        cwd=hoverpower.path.REPO,
    )


def isgit(path: str = '.'):
    completed = utilo.run(
        f'git -C {path} rev-parse --is-inside-work-tree',
        cwd=hoverpower.path.REPO,
        verbose=True,
    )
    stdout = completed.stdout.strip()
    result = 'true' in stdout
    return result
