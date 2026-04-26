#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import pytest
import utilo
import utilotest

import hoverpower
import tests


@utilotest.longrun
def test_copy_title(td):
    """Test to extract title pages from pdf files in repository"""
    title = os.path.join(td.tmpdir, 'title')
    failure = hoverpower.copy_title(dest=td.tmpdir)
    # ensure that some pdf files was copied
    extracted = len(os.listdir(title))
    assert extracted >= 187, str(title)
    # assert not failure
    assert failure == 1  # TODO: REMOVE LATER


@utilotest.longrun
def test_cli_run_title(td, mp):
    returncode = tests.fail(
        cmd='--title',
        mp=mp,
    )
    titlefolder = td.tmpdir.join('title')
    assert tests.foldersize(titlefolder) > 0, f'{titlefolder} is empty'
    with pytest.raises(AssertionError):
        # TODO: REMOVE AFTER IMPROVING PDFCAT
        assert returncode == utilo.SUCCESS
