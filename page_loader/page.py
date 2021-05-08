# -*- coding:utf-8 -*-

"""Download and save web page`s data module."""

import logging
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from page_loader import utils
from progress.bar import Bar

TAG_TO_ATTRIBUTE_MAPPING = {
    'script': 'src',
    'link': 'href',
    'img': 'src',
}
PARSER = 'html.parser'
FORMATTER = 'html5'
DIR_EXT = '_files'


def download(url: str, output: str) -> str:
    """Save requested html file with resources to given path."""
    logger = logging.getLogger('page_loader')
    html_content = get_data(url)
    html_path = os.path.join(output, utils.build_name(url))
    resources_dir = utils.build_name(url, DIR_EXT)
    html, resources_urls = prepare_resources(
        html_content,
        url,
        resources_dir,
    )
    write_to_file(html_path, html, 'w')
    logger.info('"{0}" was downloaded'.format(url))
    if resources_urls:
        resources_dir_path = os.path.join(
            output,
            utils.build_name(url, DIR_EXT),
        )
        make_dir(resources_dir_path)
        download_resources(resources_dir_path, resources_urls)
    logger.info('page saved')
    return html_path


def download_resources(download_dir: str, resources_urls: dict):
    for resource_name, resource_url in resources_urls.items():
        file_path = os.path.join(
            download_dir,
            resource_name,
        )
        content = get_data(resource_url)
        with Bar(
            'Saving "{0}"'.format(resource_url),
            max=len(content) / 1024,
        ) as progress_bar:
            write_to_file(file_path, content)
            progress_bar.next()


def get_data(url: str):
    request = requests.get(url)
    request.raise_for_status()
    return request.content


def prepare_resources(
    html: str,
    url: str,
    resources_dir,
    resources: str = TAG_TO_ATTRIBUTE_MAPPING.keys(),
):
    soup = BeautifulSoup(html, PARSER)
    tags = soup.find_all(resources)
    resources_urls = {}
    for tag in tags:
        attribute = TAG_TO_ATTRIBUTE_MAPPING[tag.name]
        tag_link = tag.get(attribute, '')
        if not tag_link or not utils.is_same_netloc(url, tag_link):
            continue
        resource_url = urljoin(
            '{0}/'.format(url),
            tag.get(attribute, ''),
        )
        resource_name = utils.build_name(resource_url)
        resources_urls[resource_name] = urljoin('{0}/'.format(url), tag_link,)

        new_link = os.path.join(
            resources_dir,
            resource_name,
        )
        tag[attribute] = new_link
    return soup.prettify(formatter=FORMATTER), resources_urls


def write_to_file(path: str, content, mode: str = 'wb'):
    with open(path, mode) as data_file:
        data_file.write(content)


def make_dir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)
