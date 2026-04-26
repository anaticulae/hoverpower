#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import importlib.metadata
import os

from resinf import Todo
from resinf import generated
from resinf import link
from resinf import prepares
from resinf import setup
from resinf import todo
from resinf import todo_new

from hoverpower.data import pdf
from hoverpower.generator import run
from hoverpower.info import bib
from hoverpower.info import ctext
from hoverpower.info import page_count
from hoverpower.info import pub
from hoverpower.title import copy_title

prepare_files = prepares

PROCESS = 'hoverpower'
__version__ = importlib.metadata.version(PROCESS)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# pylint:disable=wrong-import-position
from hoverpower.path import *  # isort:skip
from hoverpower.hard import *  # isort:skip
