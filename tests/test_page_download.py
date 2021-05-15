# -*- coding:utf-8 -*-

"""Test page download."""

import os
import pathlib
import stat
import tempfile
from urllib.parse import urljoin

import pytest
import requests
from page_loader import page

TEST_URL = 'https://page-loader.test/'
WRONG_TEST_URL = 'page-loader.test'
TEST_ASSETS = (
    'assets/src/download.png',
    'assets/src/index.js',
    'assets/styles/app.css',
)
TEST_HTML = 'test.html'
FIXTURES_DIR = 'fixtures/'
FIXTURES_ASSETS_DIR = 'assets/'
EXPECTED_PATH = 'fixtures/expected/'
EXPECTED_ASSETS_DIR = 'page-loader-test-_files'
EXPECTED_HTML_NAME = 'page-loader-test-.html'
EXPECTED_HTML_PATH = os.path.join(EXPECTED_PATH, EXPECTED_HTML_NAME)
ALLOWED_FILE_PERMISSION_CODE = stat.S_IRWXU
DENIED_FILE_PERMISSION_CODE = stat.UF_IMMUTABLE


def build_fixure_path(asset: str, asset_dir: str = '') -> str:
    file_name = os.path.basename(asset)
    return build_absolute_path(
        FIXTURES_DIR,
        asset_dir,
        file_name,
    )


def build_absolute_path(*args) -> str:
    return os.path.join(
        pathlib.Path(__file__).parent.absolute(),
        *args,
    )


def read_file(path: str, mode: str = 'rb'):
    with open(path, mode) as file:
        return file.read()


def test_download(requests_mock):
    test_html = read_file(build_fixure_path(TEST_HTML), 'r')
    requests_mock.get(TEST_URL, text=test_html)
    for asset_relative_path in TEST_ASSETS:
        fixture_path = build_fixure_path(
            asset_relative_path,
            FIXTURES_ASSETS_DIR,
        )
        fixture_content = read_file(fixture_path)
        requests_mock.get(
            urljoin(TEST_URL, asset_relative_path),
            content=fixture_content,
        )
    with tempfile.TemporaryDirectory() as tmpdirname:
        html_path = page.download(TEST_URL, tmpdirname)
        html_content = read_file(html_path, 'r')
        expected_html = read_file(
            build_absolute_path(EXPECTED_HTML_PATH),
            'r',
        )
        assert html_content == expected_html
        output_html_name, output_assets_dir = sorted(os.listdir(tmpdirname))
        assert output_html_name == EXPECTED_HTML_NAME
        output_assets_files = sorted(os.listdir(os.path.join(
            tmpdirname,
            output_assets_dir,
        )))
        expected_assets_files = sorted(os.listdir(build_absolute_path(
            EXPECTED_PATH,
            EXPECTED_ASSETS_DIR,
        )))
        assert output_assets_files == expected_assets_files
        for output_assets_file in output_assets_files:
            output_content = read_file(os.path.join(
                tmpdirname,
                output_assets_dir,
                output_assets_file,
            ))
            expected_content = read_file(build_absolute_path(
                EXPECTED_PATH,
                EXPECTED_ASSETS_DIR,
                output_assets_file,
            ))
            assert output_content == expected_content


@pytest.mark.parametrize('status_code', [
    400, 401, 403, 404, 500, 502,
])
def test_get_data_exceptions(requests_mock, status_code):
    requests_mock.get(TEST_URL, text='', status_code=status_code)
    with pytest.raises(requests.HTTPError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            page.download(TEST_URL, tmpdirname)


@pytest.mark.parametrize('url, dir, file, rights, exception', [
    (
        WRONG_TEST_URL,
        '',
        '',
        ALLOWED_FILE_PERMISSION_CODE,
        requests.exceptions.MissingSchema,
    ),
    (TEST_URL, 'dir', '', ALLOWED_FILE_PERMISSION_CODE, FileNotFoundError),
    (TEST_URL, '', '', DENIED_FILE_PERMISSION_CODE, PermissionError),
    (TEST_URL, '', 'file', ALLOWED_FILE_PERMISSION_CODE, NotADirectoryError),
])
def test_download_exceptions(
    requests_mock,
    url: str,
    dir: str,
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
        if file:
            open(os.path.join(tmpdirname, file), 'a').close()
        with pytest.raises(exception):
            page.download(url, os.path.join(tmpdirname, dir, file))
        os.chmod(tmpdirname, ALLOWED_FILE_PERMISSION_CODE)
