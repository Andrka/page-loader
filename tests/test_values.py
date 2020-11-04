# -*- coding:utf-8 -*-

"""Test values module."""

import pytest

from page_loader import values


@pytest.mark.parametrize('output_path, url, output, full_path', [
    ('', 'https://andrka.github.io/page-loader-test/', 'file', 'andrka-github-io-page-loader-test-.html'),
    ('', 'https://andrka.github.io/page-loader-test', 'file', 'andrka-github-io-page-loader-test.html'),
    ('/home', 'https://andrka.github.io/page-loader-test/', 'file', '/home/andrka-github-io-page-loader-test-.html'),
    ('/home', 'https://andrka.github.io/page-loader-test', 'file', '/home/andrka-github-io-page-loader-test.html'),
    ('', 'https://andrka.github.io/page-loader-test/', 'dir', 'andrka-github-io-page-loader-test-_files'),
    ('', 'https://andrka.github.io/page-loader-test', 'dir', 'andrka-github-io-page-loader-test_files'),
    ('/home', 'https://andrka.github.io/page-loader-test/', 'dir', '/home/andrka-github-io-page-loader-test-_files'),
    ('/home', 'https://andrka.github.io/page-loader-test', 'dir', '/home/andrka-github-io-page-loader-test_files'),
])
def test_collect_path(output_path: str, url: str, output: str, full_path: str):
    """Test collect_path function."""
    assert values.collect_path(output_path, url, output) == full_path


@pytest.mark.parametrize('url, expectation', [
    ('https://andrka.github.io/page-loader-test/', True),
    ('https://andrka.github.io/page-loader-test', True),
    ('aaa', False),
    ('andrka.github.io/page-loader-test/', False),
    ('andrka.github.io/page-loader-test', False),
    ('https://', False),
])
def test_is_correct(url: str, expectation: bool):
    """Test is_correct function."""
    assert values.is_correct(url) is expectation


def test_is_resource(soup):
    """Test is_resource function."""
    tags = soup.find_all()
    resources = 0
    for tag in tags:
        if values.is_resource(tag):
            resources += 1
    assert resources == 3
