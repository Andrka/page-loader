# -*- coding:utf-8 -*-

"""Test values module."""

import pytest

from page_loader import values


@pytest.mark.parametrize('output_path, url, file_path', [
    ('', 'https://hexlet.io/courses', 'hexlet-io-courses.html'),
    ('/home', 'https://hexlet.io/courses', '/home/hexlet-io-courses.html'),
])
def test_collect_path(output_path: str, url: str, file_path: str):
    """Test collect_path function."""
    assert values.collect_path(output_path, url) == file_path


@pytest.mark.parametrize('url, expectation', [
    ('https://hexlet.io/courses', True),
    ('aaa', False),
    ('hexlet.io/courses', False),
    ('https://', False),
])
def test_is_correct(url: str, expectation: bool):
    """Test is_correct function."""
    assert values.is_correct(url) is expectation
