# -*- coding:utf-8 -*-

"""Test page module."""

import os
import sys
import tempfile
from filecmp import dircmp
from urllib.parse import urljoin

import pytest
import requests

from page_loader import page

TEST_URL = 'https://andrka.github.io/page-loader-test/'
ASSETS_PATH = {
    'assets/src/download.png': 'fixtures/assets/download.png',
    'assets/src/index.js': 'fixtures/assets/src-index.js',
    'assets/styles/app.css': 'fixtures/assets/styles-app.css',
}
ORIGINAL_HTML_PATH = 'fixtures/original_page.html'
FULL_RESULT_PATH = 'fixtures/full_result'
FULL_RESULT_ASSETS_DIR = 'andrka-github-io-page-loader-test-_files'
RESULT_HTML_PATH = 'fixtures/full_result/andrka-github-io-page-loader-test-.html'


def collect_path(relative_path: str, current_path: str = sys.path[0]):
    return os.path.join(current_path, relative_path)


def open_text_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def open_bytes_file(path: str) -> bytes:
    with open(path, 'rb') as file:
        return file.read()


def open_fixture(path: str):
    try:
        fixture_file = open_text_file(path)
    except UnicodeDecodeError:
        fixture_file = open_bytes_file(path)
    return fixture_file


def test_download(requests_mock):
    """Test download function."""
    origin_page = open_text_file(collect_path(ORIGINAL_HTML_PATH))
    requests_mock.get(TEST_URL, text=origin_page)
    with tempfile.TemporaryDirectory() as tmpdirname:
        for asset_relative_path, fixture_relative_path in ASSETS_PATH.items():
            fixture_path = collect_path(fixture_relative_path)
            fixture_file = open_fixture(fixture_path)
            if isinstance(fixture_file, bytes):
                asset_content = open_bytes_file(fixture_path)
                requests_mock.get(
                    urljoin(TEST_URL, asset_relative_path),
                    content=asset_content,
                )
            else:
                asset_content = open_text_file(fixture_path)
                requests_mock.get(
                    urljoin(TEST_URL, asset_relative_path),
                    text=asset_content,
                )
        result_path = page.download(TEST_URL, tmpdirname)
        result_page = open_text_file(result_path)
        test_page = open_text_file(collect_path(RESULT_HTML_PATH))
        assert result_page == test_page
        result_difference = dircmp(
            tmpdirname,
            collect_path(FULL_RESULT_PATH),
        )
        assert not result_difference.left_only
        assert not result_difference.right_only
        assert not result_difference.diff_files
        result_assets_difference = dircmp(
            collect_path(FULL_RESULT_ASSETS_DIR, tmpdirname),
            collect_path(collect_path(FULL_RESULT_ASSETS_DIR, FULL_RESULT_PATH)),
        )
        assert not result_assets_difference.left_only
        assert not result_assets_difference.right_only
        assert not result_assets_difference.diff_files


@pytest.mark.parametrize('status_code', [
    '400', '401', '403', '404', '500', '502',
])
def get_data_exception(requests_mock, status_code):
    """Test exception in get_data function."""
    requests_mock.get(TEST_URL, text='', status_code=status_code)
    with pytest.raises(requests.HTTPError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            page.download(TEST_URL, tmpdirname)


@pytest.mark.parametrize('url', [
    ('andrka.github.io/page-loader-test/'),
    ('andrka.github.io/page-loader-test'),
])
def test_check_url_exception(url: str):
    """Test exception in check_url function."""
    with pytest.raises(requests.exceptions.MissingSchema):
        page.check_url(url)


def test_check_dir_existence():
    """Test dir for existence with check_dir function."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(FileNotFoundError):
            page.check_dir('{0}/false'.format(tmpdirname))


def test_create_resources_dir_rights():
    """Test for access rights with create_resources_dir function."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        path = '{0}/test'.format(tmpdirname)
        os.chmod(tmpdirname, 0o444)
        with pytest.raises(PermissionError):
            page.create_resources_dir(path)
        os.chmod(tmpdirname, 0o775)


def test_create_resources_dir_empty():
    """Test for empty dir with create_resources_dir function."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        path = '{0}/test'.format(tmpdirname)
        os.mkdir(path)
        with pytest.raises(OSError):
            page.create_resources_dir(tmpdirname)
