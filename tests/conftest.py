# -*- coding:utf-8 -*-

"""Define fixtures to use in tests."""

import os
import sys

import pytest

ORIGINAL_HTML_PATH = 'fixtures/original_page.html'
RESULT_HTML_PATH = 'fixtures/result_page.html'


@pytest.fixture(name='origin_page')
def open_origin_page() -> str:
    """Open and return for tests original html."""
    with open(os.path.join(sys.path[0], ORIGINAL_HTML_PATH), 'r') as file:
        return file.read()


@pytest.fixture(name='test_page')
def open_test_page() -> str:
    """Open and return final test page."""
    with open(os.path.join(sys.path[0], RESULT_HTML_PATH), 'r') as file:
        return file.read()
