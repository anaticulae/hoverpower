# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from hoverpower.data import collect_folder


def test_repository_folder_collector():
    collected = collect_folder()
    assert len(collected) >= 1
    assert all(isinstance(item, str) for item in collected), str(collected)
