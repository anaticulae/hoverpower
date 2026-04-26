# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""How To Use Test Data Generator
==============================

Define ``tests.conftest.PACKAGE`` to run installation process before
running extraction.

.. code-block:: python

    import pytest

    import sections
    import power

    power.setup(sections.ROOT)

    @pytest.mark.usefixtures('session')
    def pytest_sessionstart():
        power.run()

Define ``tests.conftest.extract`` hook to run test data extractor.

.. code-block:: python

    def extract():
        # single block test data extraction. Extract is only called once.
        pass

.. code-block:: python

    def extract(todo: list):
        # incremental test data generation. Extract is called with a list
        # of non existing resources
        pass

Define ``tests.conftest.RESOURCES`` to support incremental test data
generation:

.. code-block:: python

    RESOURCES = [
        (path, ),
        (path, optional:pages),
        ...
    ]

Accessing the resource(_PDF) and generated resource is very simple:

.. code-block:: python

    BACHELOR111 = power.link(power.BACHELOR111_PDF)
"""

import collections
import contextlib
import dataclasses
import functools
import importlib
import os
import re
import sys

import resinf
import resinf.configure
import utilo
import utilotest

import hoverpower

DEFAULT_STEP = '__none__'


def run(required_resources: list = None):
    assert required_resources is None or not isinstance(
        required_resources, str), 'require a list or None as input'
    if 'PYTEST_XDIST_WORKER' in os.environ:
        # master process only
        return
    # add newline
    utilo.log()
    # is generation required
    if 'GENERATE' in os.environ or utilotest.NIGHTLY:
        if not 'NOINSTALL' in os.environ:
            utilo.log('install requirements')
            install()
            utilo.log('done')
        else:
            utilo.log('skip installing requirements')
        pattern = os.environ.get('GENERATE', None)
        extract(pattern=pattern)
    if not required_resources:
        return
    utilo.log('check resources')
    check(required_resources)
    utilo.log('done')


def install():
    conftest = importlib.import_module('tests.conftest', 'tests')
    try:
        # TODO: REMOVE THIS LATER
        package = conftest.PACKAGE
    except AttributeError:
        package = resinf.mainpackage(conftest.__file__)
    if not package:
        utilo.error('could not install, define tests.conftest.PACKAGE')
        return
    utilotest.clean_install(resinf.configure.PROJECT, package)
    # run install hook after installing project
    install_after = conftest.install if hasattr(conftest, 'install') else None
    if not install_after:
        return
    utilo.log('install hook')
    with utilo.profile('done'):
        install_after()


def extract(conftest=None, pattern=None):
    """\
    >>> extract()
    """
    if conftest is None:
        conftest = importlib.import_module('tests.conftest', 'tests')
    if isinstance(pattern, str):
        pattern = pattern_compile(pattern)
    dynamics = parse_resource_definition(conftest)
    if not dynamics:
        utilo.debug('could not extract, define tests.conftest.extract')
        return
    utilo.log('extract resources')
    with utilo.profile('done'):
        parallel = [
            functools.partial(run_step, dynamic, pattern)
            for dynamic in dynamics
        ]
        with utilo.unset_env('PYTEST_PLUGINS'):  # pylint:disable=E1101
            # improve test data generation by using process pools. See
            # utilo.select_executor.
            returncode = utilo.fork(
                *parallel,
                worker=resinf.configure.WORKER,
                process=False,
            )
        # Hint: if return code is int, this indicates that some error occurs
        assert not isinstance(returncode, int), str(returncode)
    path = resinf.generated()
    if utilo.exists(path):
        # lock generated data
        utilo.directory_lock(path=path)


def pattern_compile(pattern: str):
    if pattern in {'True', 'TRUE', 'GENERATE'}:
        return None
    result = utilo.compiles(pattern)
    return result


def run_step(dynamic, pattern=None):
    parameters = utilo.attributes(dynamic.extractor)
    if not parameters:
        if os.path.exists(resinf.generated()):
            utilo.log(f'already done: {resinf.generated()}')
        else:
            utilo.log('extract resources')
            with utilo.profile('done'):
                dynamic.extractor()
        return
    # multi generator approach
    if not dynamic.resources:
        utilo.error('missing resource definition!')
        if dynamic.name == DEFAULT_STEP:
            utilo.error('define tests.conftest.RESOURCES')
        else:
            error = f'define tests.conftest.RESOURCES_{dynamic.name.upper()}'
            utilo.error(error)
        sys.exit(utilo.FAILURE)
    # determine resource folder
    folder = None if dynamic.name == DEFAULT_STEP else dynamic.name
    todos = incremental_todo(
        dynamic.resources,
        folder,
        validator=dynamic.validator,
        pattern=pattern,
    )
    if not todos:
        path = resinf.generated(dynamic.name)
        utilo.log(f'{dynamic.name} already done: {path}')
        return
    # run extractor
    if dynamic.name != DEFAULT_STEP:
        utilo.log(f'extract {dynamic.name}')
    else:
        utilo.log('extract default')
    with utilo.profile('done'):
        dynamic.extractor(todos)


RESOURCES_PATTERN = r'^RESOURCES\_{0,1}(?P<group>[_\w]{0,})'
EXTRACT_PATTERN = r'^extract\_{0,1}(?P<group>[_\w]{0,})'
VALIDATE_PATTERN = r'^validate\_{0,1}(?P<group>[_\w]{0,})'


@dataclasses.dataclass
class DynamicResource:
    name: str = None
    resources: list = None
    extractor: callable = None
    validator: callable = None


def parse_resource_definition(module) -> list:
    parsed = collections.defaultdict(DynamicResource)
    for name, value in vars(module).items():
        matched = re.match(RESOURCES_PATTERN, name)
        if matched:
            if matched['group']:
                resources = matched['group'].lower()
            else:
                resources = DEFAULT_STEP
            parsed[resources].resources = value
            parsed[resources].name = resources
            continue
        matched = re.match(EXTRACT_PATTERN, name)
        if matched:
            if matched['group']:
                resources = matched['group'].lower()
            else:
                resources = DEFAULT_STEP
            parsed[resources].extractor = value
            parsed[resources].name = resources
            continue
        matched = re.match(VALIDATE_PATTERN, name)
        if matched:
            resources = matched['group'].lower()
            parsed[resources].validator = value
            parsed[resources].name = resources
            continue
    result = list(parsed.values())
    return result


def incremental_todo(
    resources: list,
    folder: str,
    validator: callable = None,
    pattern: callable = None,
) -> list:
    if not validator:
        validator = validate_pagenumbers
    validator(resources)
    result = []
    for item in resources:
        # add support for Todo.resource
        path = item if isinstance(item, str) else item[0]
        if pattern and not pattern.search(path):
            utilo.debug(f'skip: {path} not in pattern: {pattern}')
            continue
        path = hoverpower.link(path, folder=folder)
        if not os.path.exists(str(path)):
            utilo.debug(f'missing, run generator: {path}')
            result.append(item)
    return result


def check(required_resources):
    """\
    >>> import power
    >>> check([power.link(power.MASTER116_PDF, project='foo')])
    Traceback (most recent call last):
    ...
    FileNotFoundError: run `baw --test=generate` to generate test data
    """
    error = utilo.SUCCESS
    for item in required_resources:
        if not os.path.exists(item):
            utilo.error(f'missing: {item}')
            error += 1
    advice = 'run `baw --test=generate` to generate test data'
    if error:
        raise FileNotFoundError(advice)


def validate_pagenumbers(resources: list):
    """Ensure that pagenumbers are defined correctly.

    Check that pagenumbers which are passed to rawmaker does not contain
    any whitespaces. White spaces produces an command line error when
    passing --pages flag.

    Raises:
        ValueError: If pages definition is invalid

    >>> validate_pagenumbers([('master116.pdf', '0:10')])
    >>> validate_pagenumbers([('master116.pdf', '0:10,30:40')])

    >>> validate_pagenumbers([(None, '0:10,:214:246')])
    Traceback (most recent call last):
    ...
    ValueError: invalid pages: `0:10,:214:246`

    >>> validate_pagenumbers([(None, '0 10')])
    Traceback (most recent call last):
    ...
    ValueError: invalid page number: `0 10`
    """
    # TODO: ADD MORE VALIDATION STEPS
    error = []
    for item in resources:
        pages = pagenumber(item)
        if pages is None:
            continue
        pages = str(pages).strip()
        if ' ' in pages:
            error.append(f'invalid page number: `{pages}`')
        if ',' in pages:
            if any(item.count(':') > 1 for item in pages.split(',')):
                error.append(f'invalid pages: `{pages}`')
    if not error:
        return
    raise ValueError('\n'.join(error))


def pagenumber(item) -> str:
    assert item is not None, 'check that resource is not None'
    with contextlib.suppress(AttributeError):
        return item.pages
    with contextlib.suppress(ValueError):
        _, pages = item
        return pages
    # no page definition is always right
    return None
