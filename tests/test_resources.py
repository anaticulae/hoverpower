# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilo

import hoverpower


@pytest.mark.parametrize(
    'source',
    [pytest.param(item, id=utilo.file_name(item)) for item in hoverpower.PDF],
)
def test_resource(source):
    fname = utilo.file_name(source)
    expected = utilo.parse_ints(fname)[0]
    cmd = f'pdflog -i {source}'
    completed = utilo.run(cmd)
    stdout = completed.stdout
    expected = f'"pages": {expected},'
    assert expected in stdout
