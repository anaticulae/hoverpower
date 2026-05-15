import utilo

import hoverpower.path

PROJECT = """\
[build-system]
requires = [
    "setuptools>=82.0.1",
    "wheel>=0.47.0",
]
build-backend = "setuptools.build_meta"

[project]
name = "genex"
version = "0.40.0"
description = ""
requires-python = ">=3.12"
authors = [
    { name = "Helmut Konrad Schewe", email = "helmutus@outlook.com" },
]

[project.readme]
file = "README"
content-type = "text/markdown"

[project.optional-dependencies]
dev = [
    "utilotest>=1.0.4,<2.0.0",
    "hoverpower>=1.1.0,<2.0.0",
]

[tool.hoverpower]
packages = [
    "BACHELOR",
    "DOCU",
    "HOME",
]

"""


def test_project_requires(td):
    project = utilo.join(td.tmpdir, 'pyproject.toml')
    utilo.file_create(project, PROJECT)
    requires = hoverpower.path.requires(root=td.tmpdir)
    assert requires


def test_project_requires_invalid_config(td):
    project = utilo.join(td.tmpdir, 'pyproject.toml')
    data = PROJECT.replace('packages = [', 'pack = [')
    utilo.file_create(project, data)
    requires = hoverpower.path.requires(root=td.tmpdir)
    assert not requires
