# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import pdflog.pages
import utilotest

import hoverpower.cli.give

give = functools.partial(
    utilotest.run_cov,
    main=hoverpower.cli.give.main,
    process='give',
    expect=True,
)


def test_cli_give(td, mp):
    # cmd `give master116 0:10`
    cmd = 'master116 0:10'
    give(cmd=cmd, mp=mp)
    dest = td.tmpdir.join('master116.pdf')
    pagecount = pdflog.pages.determine(dest)
    assert pagecount == 10
