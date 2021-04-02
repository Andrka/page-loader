# -*- coding:utf-8 -*-

"""Test files module."""

import tempfile
from filecmp import dircmp

import pytest

from page_loader import files

TEST_URL = 'https://andrka.github.io/page-loader-test'
FIXTURE_INDEX_PATH = 'tests/fixtures/index.html'
FIXTURES_ASSETS_PATH = {
    'download.png': 'tests/fixtures/assets/download.png',
    'src-index.js': 'tests/fixtures/assets/src-index.js',
    'styles-app.css': 'tests/fixtures/assets/styles-app.css',
}
FIXTURE_RESULT_PATH = 'tests/fixtures/result.html'


def test_download():
    """Test download function."""


# def test_save_html_exception(response):
#     """Test exception in save_html function."""
#     with pytest.raises(files.KnownError):
#         assert files.save_html('/no_permission.html', response)


# def test_save_data_exception(response):
#     """Test exception in save_data function."""
#     with pytest.raises(files.KnownError):
#         assert files.save_data('/no_permission.file', response)


# def test_save_soup_exception(soup):
#     """Test exception in save_soup function."""
#     with pytest.raises(files.KnownError):
#         assert files.save_soup('/no_permission.html', soup)


def test_make_dir_exception():
    """Test exception in make_dir function."""
    with pytest.raises(files.KnownError):
        assert files.make_dir('/no_permission')


def test_save_exception():
    """Test exception in save function."""
    url = 'error'
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(files.KnownError):
            assert files.save(tmpdirname, url)


# def test_save():
#     """Test save function."""
#     url = 'https://andrka.github.io/page-loader-test'
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         files.save(tmpdirname, url)
#         compare = dircmp(tmpdirname, 'tests/fixtures')
#         assert not compare.left_only
#         assert not compare.right_only
#         assert not compare.diff_files
