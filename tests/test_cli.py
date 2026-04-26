# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utilotest

import hoverpower
import hoverpower.cli
import tests


def test_cli_run_help(mp):
    """Simple smoke test"""
    tests.run(cmd='--help', mp=mp)


@pytest.mark.usefixtures('testdir')
def test_cli_run_list(mp, capsys):
    """Test to list content of data package"""
    tests.run(
        cmd='--list docu',
        mp=mp,
    )
    stdout = utilotest.stdout(capsys)
    assert '.pdf' in stdout, stdout


def test_cli_matches():
    """Test to list content of data package"""
    args = {
        'docu': True,
        'notexisting': True,  # negative
        'someone': False,  # negative
    }
    matched = hoverpower.cli.matches(args)
    assert len(matched) == 1, str(matched)


def test_cli_generate_docu(td, mp):
    assert not tests.foldersize(td.tmpdir), f'{td.tmpdir} is not empty'
    tests.run(
        cmd='--docu',
        mp=mp,
    )
    assert tests.foldersize(td.tmpdir) > 0, f'{td.tmpdir} is empty'


def test_cli_generate_docu_to_outputpath(td, mp):
    root = os.path.join(td.tmpdir, 'helmut')  # test output
    assert not os.path.exists(root), f'{root} is not empty'
    tests.run(
        cmd='--docu -o helmut',
        mp=mp,
    )
    assert tests.foldersize(root) > 0, f'{root} is empty'


def test_cli_generate_docu_merge_path(td, mp):
    root = td.tmpdir
    assert not tests.foldersize(td.tmpdir), f'{td.tmpdir} is not empty'
    tests.run(
        cmd='--docu --merge',
        mp=mp,
    )
    assert tests.foldersize(root) > 0, f'{root} is empty'
    error = f'merged content {root} contains folder'
    assert all(item.is_file() for item in os.scandir(root)), error


def test_cli_all(td, mp):
    """Run twice to check that skipping overwrite works"""
    assert not tests.foldersize(td.tmpdir), f'{td.tmpdir} is not empty'
    tests.run(
        cmd='--all',
        mp=mp,
    )
    # ensure that skip works
    tests.run(
        cmd='--all',
        mp=mp,
    )
    # Subtract README.md => -1
    expected = tests.foldersize(hoverpower.REPO) - 1
    assert tests.foldersize(td.tmpdir) == expected, f'{td.tmpdir} is empty'


@pytest.mark.usefixtures('testdir')
@pytest.mark.parametrize('cmd', [
    '',
    '--brokencommand',
])
def test_cli_malus_input(cmd, mp):
    tests.fail(
        cmd=cmd,
        mp=mp,
    )
