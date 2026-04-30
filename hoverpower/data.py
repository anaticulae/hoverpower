# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys

import utilo

import hoverpower


def collect_folder():
    return [
        item.name for item in os.scandir(hoverpower.STORE) if not item.is_file()
    ]


def log_available_files(package: str):
    """Log list of files/pdf containing `package` selected by user.

    >>> log_available_files('does not exist')
    Traceback (most recent call last):
    ...
    SystemExit: 1
    """
    utilo.log(f'{package}:')
    collected = collect_folder()
    if package not in collected:
        utilo.error(f'package not available: {package}')
        sys.exit(utilo.FAILURE)
    featurepath = os.path.join(hoverpower.STORE, package)
    # TODO: add recursive feature packages
    for item in os.scandir(featurepath):
        utilo.log(f'    {item.name}')


def copy_packages(matched: list, dest: str, merge: bool = False):
    """Copy select files to `dest`.

    Args:
        matched: list of selected files
        dest: directory to write files
        merge: if True, copy all files into single `dest` folder
    Raises:
        SystemExit for empty selection

    >>> copy_packages([], '.')
    Traceback (most recent call last):
    ...
    SystemExit: 1
    """
    # TODO: REPLACE WITH UTILA CODE
    if not matched:
        utilo.error('no data package selected')
        sys.exit(utilo.FAILURE)

    def copy_package(package, dest):
        """If resource already exists and is unchanged, the file is not
        touched."""
        source = os.path.join(hoverpower.STORE, package)
        utilo.copy_content(
            source,
            dest,
            update=True,  # do not change equal content
        )

    for item in matched:
        destpath = os.path.join(dest, item)
        if merge:
            # merge all pdfs to a single path
            destpath = dest
        copy_package(item, destpath)


def pdf(item):
    """Determine file path for path page tuple.

    >>> import hoverpower; hoverpower.pdf((hoverpower.DISS173_PDF, '10:45'))
    '...diss173.pdf'
    >>> import hoverpower; hoverpower.pdf(hoverpower.DISS173_PDF)
    '...diss173.pdf'
    """
    if not isinstance(item, str):
        return item[0]
    return item
