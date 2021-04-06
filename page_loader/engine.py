# -*- coding:utf-8 -*-

"""Download and save data module."""

import logging
import os
from urllib.parse import urlparse

import requests
from progress.bar import Bar

from page_loader import paths

RESOURCES = ('link', 'script', 'img')


class KnownError(Exception):
    """Known exception."""


def download(url: str, output: str) -> str:  # noqa: WPS210
    """Save requested html file with resources to given path.

    Raises:
        KnownError: exception for catching errors in main script.
    """
    logger = logging.getLogger('page_loader')
    check_url(url)
    check_dir(output)
    try:
        html_path, resources_urls = save_hltm(output, url)
    except requests.exceptions.RequestException as exc:
        raise KnownError() from exc
    logger.info('"{0}" was downloaded'.format(url))
    if resources_urls:
        create_resources_dir(
            os.path.join(output, paths.collect_dir_name(url)),
        )
        with Bar('Saving resources', max=len(resources_urls)) as progress_bar:
            for resource_url in resources_urls:
                download_dir = os.path.join(
                    output,
                    paths.collect_dir_name(url),
                )
                save_resource(resource_url, download_dir)
                progress_bar.next()  # noqa: B305
        logger.info('Page saved in: "{0}"'.format(html_path))
    return html_path


def check_url(url: str):
    """Check if the given url has full format.

    Raises:
        KnownError: exception for catching errors in main script.
    """
    parsing_url = urlparse(url)
    if not parsing_url.netloc:
        raise KnownError('"{0}": wrong url!'.format(url))


def check_dir(path: str):
    """Check if the given directory exists and has writing rights.

    Raises:
        KnownError: exception for catching errors in main script.
    """
    if not os.path.exists(path):
        raise KnownError('"{0}": directory not exist!'.format(path))
    if not os.access(path, os.W_OK):
        raise KnownError('"{0}": not access to write!'.format(path))


def create_resources_dir(path: str):
    """Create or, if exists, check for empty directory for local resources.

    Raises:
        KnownError: exception for catching errors in main script.
    """
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except (IOError, OSError) as exc:
            raise KnownError() from exc
        else:
            return
    if os.listdir(path):
        raise KnownError('"{0}": directory not empty!'.format(path))


def save_hltm(output_dir_path: str, url: str):
    """Download, change and save requested url.

    Downdoad requested url, change resources links to local paths,
    save html and return changed html path with list of resources urls.

    """
    html = get_data(url)
    html_path = os.path.join(output_dir_path, paths.collect_file_name(url))
    local_html, resources_urls = paths.change_links_to_local(
        html,
        url,
        RESOURCES,
    )
    write_to_file(html_path, local_html)
    return html_path, resources_urls


def write_to_file(path, dataset):
    """Write data to file.

    Raises:
        KnownError: exception for catching errors in main script.
    """
    if isinstance(dataset, bytes):
        try:
            with open(path, 'wb') as byte_file:
                byte_file.write(dataset)
        except (IOError, OSError) as exc:
            raise KnownError() from exc
    else:
        try:
            with open(path, 'w') as str_file:
                str_file.write(dataset)
        except (IOError, OSError) as exc:  # noqa: WPS440
            raise KnownError() from exc


def get_data(url: str):
    """Parse data from the url."""
    request = requests.get(url)
    request.raise_for_status()
    return request.content


def save_resource(url: str, download_dir: str):
    """Download and save resource."""
    logger = logging.getLogger('page_loader')
    file_path = os.path.join(download_dir, paths.collect_file_name(url))
    try:
        dataset = get_data(url)
    except requests.exceptions.RequestException as exc:
        logger.debug(exc, exc_info=True)
        logger.warning('"{0}": download failed!'.format(url))
    else:
        write_to_file(file_path, dataset)
