# -*- coding:utf-8 -*-

"""Test path module."""

import pytest

from page_loader import paths


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
def test_url_to_path(output_path: str, url: str, output: str, full_path: str):
    """Test url_to_path function."""
    assert paths.url_to_path(output_path, url, output) == full_path


@pytest.mark.parametrize('url, correct_value', [
    ('https://andrka.github.io/page-loader-test/', True),
    ('https://andrka.github.io/page-loader-test', True),
    ('aaa', False),
    ('andrka.github.io/page-loader-test/', False),
    ('andrka.github.io/page-loader-test', False),
    ('https://', False),
])
def test_is_correct(url: str, correct_value: bool):
    """Test is_correct function."""
    assert paths.is_correct(url) is correct_value
