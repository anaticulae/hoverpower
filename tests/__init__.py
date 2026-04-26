#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import utilo
import utilotest

import hoverpower

run, fail = utilotest.create_cli_runner(hoverpower)


def foldersize(path) -> int:
    """Determine the count of items in a given `path`

    Args:
        path(str): path to count items in
    Returns:
        count of items in folder
    Raises:
        ValueError: if `path` does not exists
      """
    utilo.exists_assert(path)
    return len([item.name for item in os.scandir(path)])
