# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import argparse
import os

import utilo

import hoverpower
import hoverpower.title


@utilo.saveme
def main():
    args = parse_args()
    pdf = pdf_select(name=args.pdf)
    if not pdf:
        utilo.error(f'invalid resource: {args.pdf}')
        return utilo.FAILURE
    dest = utilo.join(os.getcwd(), utilo.file_name(pdf, ext=True))
    hoverpower.title.run(
        infile=pdf,
        dest=dest,
        first_page=args.pages,
    )
    return utilo.SUCCESS


def pdf_select(name: str) -> str:
    name = name.lower()
    for pdf in hoverpower.PDF:
        fname = utilo.file_name(pdf)
        if name == fname:
            return pdf
    return None


def parse_args():
    parser = argparse.ArgumentParser(
        prog='give',
        description='Copy a document with given pages.',
    )
    parser.add_argument(
        'pdf',
        type=str,
        help='power resource',
    )
    parser.add_argument(
        'pages',
        type=str,
        nargs='?',
        default=':',
        help='resource pages',
    )
    args = parser.parse_args()
    return args
