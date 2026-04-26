# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import utilo

import hoverpower


def ctext(source: str, default=utilo.EMPTY) -> str:
    """\
    >>> import power; ctext(power.BACHELOR075_PDF)
    '14:70'

    File does not exists, use default
    >>> ctext(__file__, default=dict(pages=256))
    {'pages': 256}

    File does not exists, no default
    >>> ctext(__file__)
    Traceback (most recent call last):
    ...
    FileNotFoundError: missing file: ...
    """
    # ease interface, may want to use with page number without thinking
    # about it.
    return load_data(source, 'ctext', default)


def bib(source: str, default=utilo.EMPTY) -> str:
    """\
    >>> import power; bib(power.BACHELOR075_PDF)
    '70:75'
    >>> import power; bib(power.DISS173_PDF)
    '122:145'

    >>> bib(power.DOCU007_PDF, default='NO_BIB')
    'NO_BIB'
    """
    return load_data(source, 'bib', default)


def pub(source: str, default=utilo.EMPTY) -> str:
    """\
    >>> import power; pub(power.DISS173_PDF)
    '121'

    >>> pub(power.DOCU007_PDF, default='NO_PUB')
    'NO_PUB'
    """
    return load_data(source, 'pub', default)


def load_data(source: str, attribute: str, default=None):
    source = hoverpower.pdf(source)
    loaded = parse_info(source)
    if not loaded:
        if default != utilo.EMPTY:
            return default
        raise FileNotFoundError(f'missing file: {source}')
    value = getattr(loaded, attribute, default)
    return value


@utilo.cacheme
def parse_info(source: str):
    """\
    >>> import power; parse_info(power.BACHELOR075_PDF)
    Driver(...ctext='14:70'...)
    """
    parent = utilo.path_parent(source)
    fname = utilo.file_name(source, ext=False)
    file_info = f'{fname}info'
    path = utilo.join(parent, file_info)
    if not utilo.exists(path):
        return None
    content = utilo.file_read(path)
    data = dict([
        line.split()
        for line in content.splitlines()
        if line and '#' not in line
    ])
    result = utilo.driver(**data)
    return result


def page_count(path: str) -> int:
    r"""Determine page count out of file path.

    >>> import power; page_count(power.MASTER116_PDF)
    116
    >>> page_count(__file__)
    Traceback (most recent call last):
    ...
    ValueError: invalid file path: ...power/info.py
    """
    filename = utilo.file_name(path)
    if searched := re.search(r'(\d{1,4})', filename):
        result = int(searched[1])
        return result
    path = utilo.forward_slash(path)
    raise ValueError(f'invalid file path: {path}')
