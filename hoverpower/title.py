# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utilo

import hoverpower

PDF_EXTRACTOR = 'pdfcat'

utilo.run(f'which {PDF_EXTRACTOR}')


def copy_title(
    dest: str,
    first_page: str = '0:1',
) -> int:
    # 0:1 - first page
    dest = os.path.join(dest, 'title')
    utilo.info(f'write titles to {dest}')
    os.makedirs(dest, exist_ok=True)
    utilo.call('generate and copy titles')
    for item in hoverpower.PDF:
        utilo.info(f'collect: {item}')
    with utilo.GeorgFork(process=False) as fork:
        for item in hoverpower.PDF:
            # make output file name unique to use include parent file path
            outfile = os.path.join(dest, utilo.file_name(item))
            fork.fork(
                run,
                dest=outfile,
                infile=item,
                first_page=first_page,
            )
    if fork:
        return utilo.FAILURE
    return utilo.SUCCESS


def run(infile, dest, first_page):
    cmd = f'{PDF_EXTRACTOR} -o {dest} {infile} {first_page}'
    completed = utilo.run(
        cmd,
        expect=None,
    )
    if completed.returncode:
        utilo.error(f'could not extract {infile} to {dest}')
