# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower

RESOURCES = [
    (os.path.join(hoverpower.REPO, 'resources/first.pdf'), '10:20'),
    (os.path.join(hoverpower.REPO, 'resources/third.pdf'), '10:20'),
    os.path.join(hoverpower.REPO, 'resources/fourth.pdf'),
]


def extract(_):  # pylint:disable=W0613
    pass
