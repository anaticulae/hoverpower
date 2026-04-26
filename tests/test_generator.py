# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import hoverpower.generator
import tests.data.incremental_update
import tests.data.multiple_generator


def test_extract_incremental_no_resources(capsys):
    conftest = hoverpower.generator
    with pytest.raises(SystemExit):
        hoverpower.generator.extract(conftest)
    _, stderr = capsys.readouterr()
    assert 'define tests.conftest.RESOURCES' in stderr


def test_extract_incremental_full(mp):
    conftest = tests.data.incremental_update

    def extract(resources):
        # resources exists, but the expected generated folders not.
        assert len(resources) == 3, str(resources)

    with mp.context() as context:
        context.setattr(tests.data.incremental_update, 'extract', extract)
        hoverpower.generator.extract(conftest)


def test_extract_incremental_pattern(mp):
    # first.pdf third.pdf, skip second
    pattern = r'[d|t]\.pdf'
    conftest = tests.data.incremental_update

    def extract(resources):
        # first.pdf third.pdf, skip second
        assert len(resources) == 2, str(resources)

    with mp.context() as context:
        context.setattr(tests.data.incremental_update, 'extract', extract)
        hoverpower.generator.extract(conftest, pattern=pattern)


def test_single_step_generator_approach(mp):
    conftest = tests.data.incremental_update

    def extract():
        pass

    with mp.context() as context:
        context.setattr(tests.data.incremental_update, 'extract', extract)
        hoverpower.generator.extract(conftest)


def test_multiple_generator_definition():
    conftest = tests.data.multiple_generator

    parsed = hoverpower.generator.parse_resource_definition(conftest)
    assert len(parsed) == 3
    names = sorted([item.name for item in parsed])
    expected = [hoverpower.generator.DEFAULT_STEP, 'alpha', 'beta']
    assert names == expected
