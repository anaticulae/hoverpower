import argparse
import os

import utilo

import hoverpower.path


@utilo.saveme
def main():
    args = parse_args()
    root = os.getcwd()
    store = args.store
    packages = args.packages
    hoverpower.path.download_packages(
        root=root,
        source=store,
        packages=packages,
    )
    return utilo.SUCCESS


def parse_args():
    parser = argparse.ArgumentParser(
        prog='powerdownload',
        description='downloads given resources from github',
    )
    parser.add_argument(
        '--store',
        type=str,
        default=None,
        help='dest for downloading',
    )
    parser.add_argument(
        'packages',
        type=str,
        nargs='?',
        default='None',
        help='selected resources to download',
    )
    args = parser.parse_args()
    return args
