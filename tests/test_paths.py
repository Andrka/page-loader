# -*- coding:utf-8 -*-

"""Test path module."""

import pytest

from page_loader import paths
from page_loader.engine import RESOURCES
from tests.test_engine import TEST_URL

RESOURCES_URLS = (
    'https://andrka.github.io/page-loader-test/assets/src/download.png',
    'https://andrka.github.io/page-loader-test/assets/src/index.js',
    'https://andrka.github.io/page-loader-test/assets/styles/app.css',
)


@pytest.mark.parametrize('url, result', [
    ('https://andrka.github.io/page-loader-test/', 'andrka-github-io-page-loader-test-.html'),
    ('https://andrka.github.io/page-loader-test', 'andrka-github-io-page-loader-test.html'),
    ('https://andrka.github.io/page-loader-test/assets/src/download.png', 'andrka-github-io-page-loader-test-assets-src-download.png'),
    ('https://andrka.github.io/page-loader-test/assets/src/index.js', 'andrka-github-io-page-loader-test-assets-src-index.js'),
    ('https://andrka.github.io/page-loader-test/assets/styles/app.css', 'andrka-github-io-page-loader-test-assets-styles-app.css'),
])
def test_collect_file_name(url: str, result: str):
    """Test collect_file_name function."""
    assert paths.collect_file_name(url) == result


@pytest.mark.parametrize('string, result', [
    ('https://andrka.github.io/page-loader-test/', 'https-andrka-github-io-page-loader-test-'),
    ('https://andrka.github.io/page-loader-test', 'https-andrka-github-io-page-loader-test'),
    ('https://andrka.github.io/page-loader-test/assets/src/download.png', 'https-andrka-github-io-page-loader-test-assets-src-download-png'),
    ('https://andrka.github.io/page-loader-test/assets/src/index.js', 'https-andrka-github-io-page-loader-test-assets-src-index-js'),
    ('https://andrka.github.io/page-loader-test/assets/styles/app.css', 'https-andrka-github-io-page-loader-test-assets-styles-app-css'),
])
def test_replace_symbols(string: str, result: str):
    """Test replace_symbols function."""
    assert paths.replace_symbols(string) == result


def test_change_links_to_local(origin_page: str, test_page: str):
    """Test chahge_links_to_local function."""
    result_page, result_resources_urls = paths.change_links_to_local(
        origin_page,
        TEST_URL,
        RESOURCES,
    )
    assert result_page == test_page
    assert set(result_resources_urls) == set(RESOURCES_URLS)


@pytest.mark.parametrize(('url', 'link', 'result'), [
    ('https://andrka.github.io/page-loader-test/', 'assets/src/download.png', True),
    ('https://andrka.github.io/page-loader-test/', 'https://andrka.github.io/page-loader-test/assets/src/download.png', True),
    ('https://andrka.github.io/page-loader-test/', 'assets/src/index.js', True),
    ('https://andrka.github.io/page-loader-test/', 'https://andrka.github.io/page-loader-test/assets/src/index.js', True),
    ('https://andrka.github.io/page-loader-test/', 'assets/styles/app.css', True),
    ('https://andrka.github.io/page-loader-test/', 'https://andrka.github.io/page-loader-test/assets/styles/app.css', True),
    ('https://andrka.github.io/page-loader-test/', 'https://www.google.com/images', False),
    ('https://andrka.github.io/page-loader-test/', 'https://code.jquery.com/jquery-3.3.1.slim.min.js', False),
])
def test_is_local_link(url: str, link: str, result: bool):
    """Test is_local_link function."""
    assert paths.is_local_link(url, link) == result


@pytest.mark.parametrize('url, result', [
    ('https://andrka.github.io/page-loader-test/', 'andrka-github-io-page-loader-test-_files'),
    ('https://andrka.github.io/page-loader-test', 'andrka-github-io-page-loader-test_files'),
    ('https://andrka.github.io/page-loader-test/assets/src/', 'andrka-github-io-page-loader-test-assets-src-_files'),
    ('https://andrka.github.io/page-loader-test/assets/src', 'andrka-github-io-page-loader-test-assets-src_files'),
    ('https://andrka.github.io/page-loader-test/assets/styles/', 'andrka-github-io-page-loader-test-assets-styles-_files'),
    ('https://andrka.github.io/page-loader-test/assets/styles', 'andrka-github-io-page-loader-test-assets-styles_files'),
])
def test_collect_dir_name(url: str, result: str):
    """Test collect_dir_name function."""
    assert paths.collect_dir_name(url) == result
