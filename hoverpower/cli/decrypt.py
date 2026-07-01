import argparse

import utilo

import hoverpower.secret


@utilo.saveme
def main():
    args = parse_args()
    overwrite = args.overwrite
    hoverpower.secret.make_public(overwrite=overwrite)
    return utilo.SUCCESS


def parse_args():
    parser = argparse.ArgumentParser(
        prog='powerdecrypt',
        description='Decrypt all pdf files',
    )
    parser.add_argument(
        '--overwrite',
        action="store_true",
        help='decrypt files again',
    )
    args = parser.parse_args()
    return args
