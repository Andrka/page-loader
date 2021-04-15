# -*- coding:utf-8 -*-

"""Test page download."""

import os
import sys
import tempfile
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
        result_dir_entry = sorted(os.listdir(tmpdirname))
        expected_dir_entry = sorted(os.listdir(
            os.path.join(sys.path[0], EXPECTED_PATH),
        ))
        assert result_dir_entry == expected_dir_entry
        result_assets_dir = [entry.name for entry in os.scandir(
            tmpdirname,
        ) if entry.is_dir()][0]
        result_assets_entry = sorted(os.listdir(os.path.join(
            tmpdirname,
            result_assets_dir,
        )))
        expected_assets_entry = sorted(os.listdir(os.path.join(
            sys.path[0],
            EXPECTED_PATH,
            EXPECTED_ASSETS_DIR,
        )))
        assert result_assets_entry == expected_assets_entry
        for entry in result_assets_entry:
            result_asset = open_fixture(os.path.join(
                tmpdirname,
                result_assets_dir,
                entry,
            ))
            expected_asset = open_fixture(os.path.join(
                sys.path[0],
                EXPECTED_PATH,
                EXPECTED_ASSETS_DIR,
                entry,
            ))
            assert result_asset == expected_asset


@pytest.mark.parametrize('status_code', [
    400, 401, 403, 404, 500, 502,
])
def test_get_data_exceptions(requests_mock, status_code):
    requests_mock.get(TEST_URL, text='', status_code=status_code)
    with pytest.raises(requests.HTTPError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            page.download(TEST_URL, tmpdirname)


@pytest.mark.parametrize('url, dir, subdir, file, rights, exception', [
    ('page-loader.test', '', '', '', 0o775, requests.exceptions.MissingSchema),
    ('https://page-loader.test/', 'dir', '', '', 0o775, FileNotFoundError),
    ('https://page-loader.test/', '', '', '', 0o444, PermissionError),
    ('https://page-loader.test/', '', '', 'file', 0o775, NotADirectoryError),
    ('https://page-loader.test/', '', 'subdir', '', 0o775, OSError),
])
def test_download_exceptions(
    requests_mock,
    url: str,
    dir: str,
    subdir: str,
    file: str,
    rights,
    exception,
):
    with tempfile.TemporaryDirectory() as tmpdirname:
        requests_mock.get(
            url,
            text='<script src="page-loader-test-_files/test">',
        )
        os.chmod(tmpdirname, rights)
        if subdir:
            os.makedirs(os.path.join(
                tmpdirname,
                EXPECTED_ASSETS_DIR,
                subdir,
            ))
        if file:
            open(os.path.join(tmpdirname, file), 'a').close()
        with pytest.raises(exception):
            page.download(url, os.path.join(tmpdirname, dir, file))
        os.chmod(tmpdirname, 0o775)
