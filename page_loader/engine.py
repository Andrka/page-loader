# -*- coding:utf-8 -*-

"""Download and save data module."""

import logging
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader import paths


class KnownError(Exception):
    """Known exception."""


def download(url: str, output: str) -> str:
    """Save requested html file with resources to given path."""


def load(url: str):
    """Downdoad requested url and return Response object."""
    return requests.get(url)


def parse_html(path: str):
    """Parse given html file to BeautifulSoup object."""
    with open(path) as html:
        return BeautifulSoup(html, 'html.parser')


def save_html(output: str, load_data):
    """Save given Response object in html to output path.

    Raises:
        KnownError: exception for catching errors in main script.
    """
    try:
        with open(output, 'w') as output_file:
            output_file.write(load_data.text)
    except (IOError, OSError) as exc:
        raise KnownError() from exc


def save_data(output: str, load_data):
    """Save given data from Response object to output path.

    Raises:
        KnownError: exception for catching errors in main script.
    """
    try:
        with open(output, 'wb') as output_file:
            output_file.write(load_data.content)
    except (IOError, OSError) as exc:
        raise KnownError() from exc


def save_soup(output: str, soup):
    """Save BeautifulSoup object to output path.

    Raises:
        KnownError: exception for catching errors in main script.
    """
    try:
        with open(output, 'wb') as output_file:
            output_file.write(soup.encode('utf-8'))
    except (IOError, OSError) as exc:
        raise KnownError() from exc


def make_dir(path: str):
    """Create directory.

    Raises:
        KnownError: exception for catching errors in main script.
    """
    try:
        os.mkdir(path)
    except (IOError, OSError) as exc:
        raise KnownError() from exc


def download_page(  # noqa: WPS210, WPS213, WPS231
    output: str,
    url: str,
) -> str:
    """Save requested html file with resources to given path.

    Raises:
        KnownError: exception for catching errors in main script.
    """
    logger = logging.getLogger('page_loader')
    try:
        load_data = load(url)
    except requests.RequestException as exc:
        raise KnownError() from exc
    html_path = paths.url_to_path(output, url)
    if not os.path.isdir(output):
        make_dir(output)
    save_html(html_path, load_data)
    logger.info('"{0}" was saved'.format(os.path.basename(html_path)))
    soup = parse_html(html_path)
    output_dir = paths.url_to_path(output, url, 'dir')
    if not os.path.isdir(output_dir):
        make_dir(output_dir)
    resources = soup.find_all(paths.is_local_asset)
    if url[-1] != '/':
        url = '{0}/'.format(url)
    bar_level = len(resources)
    with Bar('Saving resources', max=bar_level) as bar:  # noqa: WPS110
        for resource in resources:
            resource_url = urljoin(url, resource[paths.ATTR])
            try:
                load_data = load(resource_url)
            except requests.RequestException as exc:  # noqa: WPS440
                logger.warning('"{0}" can`t be downloaded: {1}'.format(
                    resource_url,
                    exc,
                ))
                del resource[paths.ATTR]  # noqa: WPS420
            else:
                resource_path, extension = os.path.splitext(
                    resource[paths.ATTR],
                )
                data_path = paths.url_to_path(
                    output_dir,
                    resource_path,
                    'file',
                    extension,
                )
                save_data(data_path, load_data)
                _, resource_name = os.path.split(data_path)
                resource[paths.ATTR] = os.path.join(
                    os.path.basename(os.path.normpath(output_dir)),
                    resource_name,
                )
                save_soup(html_path, soup)
            bar.next()  # noqa: B305
    return html_path
