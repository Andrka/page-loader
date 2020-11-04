# -*- coding:utf-8 -*-

"""Define fixtures to use in tests."""

import pytest
from bs4 import BeautifulSoup


@pytest.fixture(name='soup')
def load_soup():
    """Return BeautifulSoup object for tests."""
    with open('tests/fixtures/andrka-github-io-page-loader-test.html') as html:
        return BeautifulSoup(html, 'html.parser')
