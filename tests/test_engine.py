# -*- coding:utf-8 -*-

"""Test engine module."""

import os
import sys
import tempfile
from filecmp import dircmp
from urllib.parse import urljoin

import pytest
import requests_mock

from page_loader import engine

TEST_URL = 'https://andrka.github.io/page-loader-test/'
ASSETS_PATH = {
    'assets/src/download.png': ('fixtures/assets/download.png', 'rb'),
    'assets/src/index.js': ('fixtures/assets/src-index.js', 'r'),
    'assets/styles/app.css': ('fixtures/assets/styles-app.css', 'r'),
}
FULL_RESULT_PATH = 'fixtures/full_result'
FULL_RESULT_ASSETS_DIR = 'andrka-github-io-page-loader-test-_files'


def test_download(origin_page, test_page):
    """Test download function."""
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
                        urljoin(TEST_URL, asset_path),
                        content=asset_content,
                    )
                else:
                    m.get(
                        urljoin(TEST_URL, asset_path),
                        text=asset_content,
                    )
            result_path = engine.download(TEST_URL, tmpdirname)
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


def test_download_exception():
    """Test exception in download function."""
    with pytest.raises(engine.KnownError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            engine.download('http://falseurl.falseurl', tmpdirname)


@pytest.mark.parametrize('url', [
    ('andrka.github.io/page-loader-test/'),
    ('andrka.github.io/page-loader-test'),
])
def test_check_url_exception(url: str):
    """Test exception in check_url function."""
    with pytest.raises(engine.KnownError):
        engine.check_url(url)


def test_check_dir_existence():
    """Test dir for existence with check_dir function."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(engine.KnownError):
            engine.check_dir('{0}/false'.format(tmpdirname))


def test_check_dir_for_write():
    """Test dir for access to write in check_dir function."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chmod(tmpdirname, 0o444)
        with pytest.raises(engine.KnownError):
            engine.check_dir(tmpdirname)
        os.chmod(tmpdirname, 0o775)


def test_create_resources_dir_rights():
    """Test for access rights with create_resources_dir function."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        path = '{0}/test'.format(tmpdirname)
        os.chmod(tmpdirname, 0o444)
        with pytest.raises(engine.KnownError):
            engine.create_resources_dir(path)
        os.chmod(tmpdirname, 0o775)


def test_create_resources_dir_empty():
    """Test for empty dir with create_resources_dir function."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        path = '{0}/test'.format(tmpdirname)
        os.mkdir(path)
        with pytest.raises(engine.KnownError):
            engine.create_resources_dir(tmpdirname)


@pytest.mark.parametrize('dataset', [
    (b'test_string'),
    ('test_string'),
])
def test_write_to_file(dataset):
    """Test exception in write_to_file function."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        path = '{0}/test'.format(tmpdirname)
        os.chmod(tmpdirname, 0o444)
        with pytest.raises(engine.KnownError):
            engine.write_to_file(path, dataset)
        os.chmod(tmpdirname, 0o775)
