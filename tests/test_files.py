# -*- coding:utf-8 -*-

"""Test files module."""

import tempfile
from filecmp import dircmp

from page_loader import files


def test_save():
    """Test save function."""
    url = 'https://andrka.github.io/page-loader-test'
    with tempfile.TemporaryDirectory() as tmpdirname:
        files.save(tmpdirname, url)
        compare = dircmp(tmpdirname, 'tests/fixtures')
        assert not compare.left_only
        assert not compare.right_only
        assert not compare.diff_files