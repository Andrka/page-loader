# -*- coding:utf-8 -*-

"""Download and save web page`s data module."""

import logging
import os
from urllib.parse import urlparse

import requests
from page_loader import utils
from progress.bar import Bar

RESOURCES = ('link', 'script', 'img')


def download(url: str, output: str) -> str:  # noqa: WPS210
    """Save requested html file with resources to given path."""
    logger = logging.getLogger('page_loader')
    check_url(url)
    check_dir(output)
    html_path, resources_urls = save_hltm(output, url)
    logger.info('"{0}" was downloaded'.format(url))
    if resources_urls:
        create_resources_dir(
            os.path.join(output, utils.collect_dir_name(url)),
        )
        with Bar('Saving resources', max=len(resources_urls)) as progress_bar:
            for resource_url in resources_urls:
                download_dir = os.path.join(
                    output,
                    utils.collect_dir_name(url),
                )
                save_resource(resource_url, download_dir)
                progress_bar.next()  # noqa: B305
    logger.info('page saved')
    return html_path


def check_url(url: str):
    """Check if the given url has full format.

    Raises:
        MissingSchema: url without schema.
    """
    parsing_url = urlparse(url)
    if not parsing_url.netloc:
        raise requests.exceptions.MissingSchema(
            '"{0}": wrong url!'.format(url),
        )


def check_dir(path: str):
    """Check if the given directory exists and has writing rights.

    Raises:
        FileNotFoundError: directory not exists.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            '"{0}": directory does not exist!'.format(path),
        )


def create_resources_dir(path: str):
    """Create or, if exists, check for empty directory for local resources.

    Raises:
        OSError: directory not empty.
    """
    if not os.path.exists(path):
        os.mkdir(path)
    if os.listdir(path):
        raise OSError('"{0}": directory not empty!'.format(path))


def save_hltm(output_dir_path: str, url: str):
    """Download, change and save requested url.

    Downdoad requested url, change resources links to local utils,
    save html and return changed html path with list of resources urls.

    """
    html = get_data(url)
    html_path = os.path.join(output_dir_path, utils.collect_file_name(url))
    local_html, resources_urls = utils.change_links_to_local(
        html,
        url,
        RESOURCES,
    )
    write_to_file(html_path, local_html)
    return html_path, resources_urls


def write_to_file(path, dataset):
    """Write data to file."""
    if isinstance(dataset, bytes):
        with open(path, 'wb') as byte_file:
            byte_file.write(dataset)
    else:
        with open(path, 'w') as str_file:
            str_file.write(dataset)


def get_data(url: str):
    """Parse data from the url."""
    request = requests.get(url)
    request.raise_for_status()
    return request.content


def save_resource(url: str, download_dir: str):
    """Download and save resource."""
    logger = logging.getLogger('page_loader')
    file_path = os.path.join(download_dir, utils.collect_file_name(url))
    try:
        dataset = get_data(url)
    except requests.exceptions.RequestException as exc:
        logger.debug(exc, exc_info=True)
        logger.warning('"{0}": download failed!'.format(url))
    else:
        write_to_file(file_path, dataset)
