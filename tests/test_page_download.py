# -*- coding:utf-8 -*-

"""Test page download."""

import os
import sys
import tempfile
from filecmp import dircmp
from urllib.parse import urljoin

import pytest
import requests
from page_loader import page, utils

TEST_URL = 'https://page-loader.test/'
TEST_ASSETS = (
    'assets/src/download.png',
    'assets/src/index.js',
    'assets/styles/app.css',
)
BYTES_EXT = ('.png', )
TEST_HTML = 'test.html'
HTML_EXT = os.path.splitext(TEST_HTML)[1]
FIXTURES_DIR = 'fixtures/'
FIXTURES_ASSETS_DIR = 'fixtures/assets/'
EXPECTED_PATH = 'fixtures/expected/'
EXPECTED_ASSETS_DIR = utils.collect_dir_name(TEST_URL)
EXPECTED_HTML_NAME = utils.collect_file_name(TEST_URL)
EXPECTED_HTML_PATH = os.path.join(EXPECTED_PATH, EXPECTED_HTML_NAME)


def collect_fixture_path(asset: str) -> str:
    file_name = os.path.basename(asset)
    file_ext = os.path.splitext(file_name)[1]
    if file_ext == HTML_EXT:
        return os.path.join(FIXTURES_DIR, file_name)
    return os.path.join(FIXTURES_ASSETS_DIR, file_name)


def open_file(path: str, mode: str = 'r') -> str:
    with open(path, mode) as file:
        return file.read()


def open_fixture(path: str):
    file_ext = os.path.splitext(path)[1]
    if file_ext in BYTES_EXT:
        return open_file(path, 'rb')
    return open_file(path)


def test_download(requests_mock):
    """Test download function."""
    test_page = open_file(os.path.join(
        sys.path[0],
        collect_fixture_path(TEST_HTML),
    ))
    requests_mock.get(TEST_URL, text=test_page)
    for asset_relative_path in TEST_ASSETS:
        fixture_relative_path = collect_fixture_path(asset_relative_path)
        fixture_path = os.path.join(sys.path[0], fixture_relative_path)
        fixture_file = open_fixture(fixture_path)
        content_file = fixture_file.encode('utf-8') if isinstance(
            fixture_file,
            str,
        ) else fixture_file
        requests_mock.get(
            urljoin(TEST_URL, asset_relative_path),
            content=content_file,
        )
    with tempfile.TemporaryDirectory() as tmpdirname:
        result_path = page.download(TEST_URL, tmpdirname)
        result_page = open_file(result_path)
        expected_page = open_file(os.path.join(
            sys.path[0],
            EXPECTED_HTML_PATH,
        ))
        assert result_page == expected_page
        expected_difference = dircmp(
            tmpdirname,
            os.path.join(sys.path[0], EXPECTED_PATH),
        )
        assert not expected_difference.left_only
        assert not expected_difference.right_only
        assert not expected_difference.diff_files
        expected_assets_difference = dircmp(
            os.path.join(tmpdirname, EXPECTED_ASSETS_DIR),
            os.path.join(
                sys.path[0],
                os.path.join(EXPECTED_PATH, EXPECTED_ASSETS_DIR),
            ),
        )
        assert not expected_assets_difference.left_only
        assert not expected_assets_difference.right_only
        assert not expected_assets_difference.diff_files


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
