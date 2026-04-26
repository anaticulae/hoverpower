#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""cli
===

TODO: add method to check that no resources conflict when using --merge
TODO: add recursive packages

"""

import os

import utilo

import hoverpower
import hoverpower.data

LIST_FEATURES = 'list'

COMMANDS = [
    utilo.Parameter(
        longcut='list',
        message='list all available resources in group',
    ),
    utilo.Flag(
        longcut='merge',
        message='merge output to single path',
    ),
    utilo.Flag(
        longcut='all',
        message='copy all data packages',
    ),
    utilo.Flag(
        longcut='title',
        message='generate title pages for every defined document',
    ),
]


@utilo.saveme
def main():
    parser = create_parser()
    args = utilo.parse(parser)
    if listfeature := args.get('list'):
        hoverpower.data.log_available_files(listfeature)
        return utilo.SUCCESS
    outputpath = utilo.sources(args)[1]
    # the default outputpath is the current working directory
    outputpath = outputpath if outputpath else os.getcwd()
    done = False
    if args.get('title'):
        if failure := hoverpower.copy_title(dest=outputpath):
            return failure
        done = True
    matched = matches(args)
    if matched:
        hoverpower.data.copy_packages(
            matched=matched,
            dest=outputpath,
            merge=args.get('merge'),
        )
        return utilo.SUCCESS
    if done:
        # Something was done
        return utilo.SUCCESS
    # nothing was selected by the user, print help and exit with failure
    parser.print_help()
    return utilo.FAILURE


def create_parser():
    cmds = cmdline_from_repository() + COMMANDS
    parser = utilo.create_parser(
        todo=cmds,
        config=utilo.ParserConfiguration(
            inputparameter=False,
            outputparameter=True,
            prefix=False,
            waitingflag=False,
            cacheflag=False,
            pages=False,
        ),
        version=hoverpower.__version__,
    )
    return parser


def cmdline_from_repository():
    """Create a list out of repository data to copy the folder by user
    command"""
    result = [
        utilo.Flag(longcut=name, message=f'copy data {name}')
        for name in hoverpower.data.collect_folder()
    ]
    return result


def matches(args):
    """Determine selected `args` which match with repository data package in
    repository"""
    collected = hoverpower.data.collect_folder()
    all_packages = args.get('all', False)
    result = [
        item for item, state in args.items()
        if (state or all_packages) and item in collected
    ]
    return result
