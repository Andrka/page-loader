# -*- coding:utf-8 -*-

"""Test engine module."""

import tempfile
from filecmp import dircmp
import requests_mock
import pytest
import os
import sys

from page_loader import engine

TEST_URL = 'https://andrka.github.io/page-loader-test'
ORIGINAL_HTML_PATH = 'fixtures/original_page.html'
ASSETS_PATH = {
    'assets/src/download.png': ('fixtures/assets/download.png', 'rb'),
    'assets/src/index.js': ('fixtures/assets/src-index.js', 'r'),
    'assets/styles/app.css': ('fixtures/assets/styles-app.css', 'r'),
}
RESULT_HTML_PATH = 'fixtures/result_page.html'
FULL_RESULT_PATH = 'fixtures/full_result'
FULL_RESULT_ASSETS_DIR = 'andrka-github-io-page-loader-test_files'


def test_download():
    """Test download function."""
    with open(os.path.join(sys.path[0], ORIGINAL_HTML_PATH), 'r') as file:
        origin_page = file.read()
    with open(os.path.join(sys.path[0], RESULT_HTML_PATH), 'r') as file:
        test_page = file.read()
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(TEST_URL, text=origin_page)
            for asset_path, asset_fixture in ASSETS_PATH.items():
                with open(
                    os.path.join(sys.path[0], asset_fixture[0]),
                    asset_fixture[1],
                ) as asset_data:
                    asset_content = asset_data.read()
                if asset_fixture[1] == 'rb':
                    m.get(
                        os.path.join(TEST_URL, asset_path),
                        content=asset_content,
                    )
                else:
                    m.get(
                        os.path.join(TEST_URL, asset_path),
                        text=asset_content,
                    )
            # result_path = engine.download(TEST_URL, tmpdirname)
            result_path = engine.download_page(output=tmpdirname, url=TEST_URL)
        with open(result_path, 'r') as file:
            result_page = file.read()
        assert result_page == test_page
        result_difference = dircmp(
            tmpdirname,
            os.path.join(sys.path[0], FULL_RESULT_PATH),
        )
        assert not result_difference.left_only
        assert not result_difference.right_only
        assert not result_difference.diff_files
        result_assets_difference = dircmp(
            os.path.join(tmpdirname, FULL_RESULT_ASSETS_DIR),
            os.path.join(sys.path[0], os.path.join(
                FULL_RESULT_PATH,
                FULL_RESULT_ASSETS_DIR,
            )),
        )
        assert not result_assets_difference.left_only
        assert not result_assets_difference.right_only
        assert not result_assets_difference.diff_files


# def test_save_html_exception(response):
#     """Test exception in save_html function."""
#     with pytest.raises(engine.KnownError):
#         assert engine.save_html('/no_permission.html', response)


# def test_save_data_exception(response):
#     """Test exception in save_data function."""
#     with pytest.raises(engine.KnownError):
#         assert engine.save_data('/no_permission.file', response)


# def test_save_soup_exception(soup):
#     """Test exception in save_soup function."""
#     with pytest.raises(engine.KnownError):
#         assert engine.save_soup('/no_permission.html', soup)


def test_make_dir_exception():
    """Test exception in make_dir function."""
    with pytest.raises(engine.KnownError):
        assert engine.make_dir('/no_permission')


def test_save_exception():
    """Test exception in save function."""
    url = 'error'
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(engine.KnownError):
            assert engine.download_page(tmpdirname, url)
