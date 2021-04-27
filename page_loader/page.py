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
    html = get_data(url)
    html_path = os.path.join(output, utils.build_name(url))
    resources_dir = utils.build_name(url, DIR_EXT)
    resources_urls = []
    local_html = prepare_resources(
        html,
        url,
        TAG_TO_ATTRIBUTE_MAPPING.keys(),
        resources_dir,
        resources_urls,
    )
    write_to_file(html_path, local_html, 'w')
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


def download_resources(download_dir, resources_urls):
    for resource_url in resources_urls:
        file_path = os.path.join(
            download_dir,
            utils.build_name(resource_url),
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
    resources,
    resources_dir,
    resources_urls,
):
    soup = BeautifulSoup(html, PARSER)
    tags = soup.find_all(resources)
    for tag in tags:
        attribute = TAG_TO_ATTRIBUTE_MAPPING[tag.name]
        tag_link = tag.get(attribute, '')
        if not tag_link:
            continue
        if utils.is_same_netloc(url, tag_link):
            resources_urls.append(
                urljoin(
                    '{0}/'.format(url),
                    tag_link,
                ),
            )
            resource_url = urljoin(
                url,
                tag.get(attribute, ''),
            )
            new_link = os.path.join(
                resources_dir,
                utils.build_name(resource_url),
            )
            tag[attribute] = new_link
    return soup.prettify(formatter=FORMATTER)


def write_to_file(path: str, content, mode: str = 'wb'):
    with open(path, mode) as data_file:
        data_file.write(content)


def make_dir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)
