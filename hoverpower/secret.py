# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import re

import cryptography.fernet
import utilo

import hoverpower.path

DEFAULT_SECRET = b'ohrfFMW4YeHu96rkblrD-i4PEIsV_5jFCfZWfgkUgLk='

HOVERPOWER_SECRET = os.environ.get('HOVERPOWER_SECRET', DEFAULT_SECRET)

CIPHER = cryptography.fernet.Fernet(key=HOVERPOWER_SECRET)


def decrypt(path: str) -> bytes | None:
    """Read encypted file content and make it raw."""
    encrypted = utilo.file_read_binary(path)
    try:
        data = CIPHER.decrypt(encrypted)
    except cryptography.fernet.InvalidToken:
        utilo.error(f'invalid HOVERPOWER_SECRET for {path}')
        return None
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
    utilo.log(f'store: {hoverpower.path.STORE}')
    for source in hoverpower.path.RESOURCES:
        if 'https://' in source:
            continue
        if '.pdf' not in source:
            continue
        source = source.replace('.pdf', '.pdfs')
        if not utilo.exists(source):
            utilo.log(f'does not exist: {source}')
            continue
        utilo.log(source)
        public = decrypt(source)
        if not public:
            continue
        base, fname = ensure_parant(source)
        outpath = utilo.join(base, fname.replace('.pdfs', '.pdf'))
        utilo.log(f'=> {outpath}')
        utilo.file_replace_binary(
            path=outpath,
            content=public,
        )
        copy_fileinfo(source)


def copy_fileinfo(source: str):
    base, fname = ensure_parant(source)
    assert fname.endswith('.pdfs'), fname
    fname = fname.replace('.pdfs', 'info')
    path = utilo.join(utilo.path_parent(source), fname)
    if not utilo.exists(path):
        return
    content = utilo.file_read(path)
    outpath = utilo.join(base, fname)
    utilo.log(f'write: {outpath}')
    utilo.file_replace(outpath, content)


def ensure_parant(source: str):
    fname = utilo.file_name(source, ext=True)
    # bachelor124.pdfs => bachelor/bachelor124.pdf
    base = utilo.join(
        hoverpower.path.STORE,
        re.split(r'(?=\d)', fname)[0],
    )
    os.makedirs(base, exist_ok=True)
    return base, fname


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
