# -*- coding:utf-8 -*-

"""Download and save web page`s data module."""

import logging
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from page_loader import utils
from progress.bar import Bar

LINK = 'link'
HREF = 'href'
SRC = 'src'
RESOURCES = (LINK, 'script', 'img')
PARSER = 'html.parser'
FORMATTER = 'html5'
DIR_EXT = '_files'


def download(url: str, output: str) -> str:
    """Save requested html file with resources to given path."""
    logger = logging.getLogger('page_loader')
    html = get_data(url)
    html_path = os.path.join(output, utils.build_name(url))
    local_html, resources_urls = change_links_to_local(
        html,
        url,
        RESOURCES,
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
    with Bar('Saving resources', max=len(resources_urls)) as progress_bar:
        for resource_url in resources_urls:
            save_resource(resource_url, download_dir)
            progress_bar.next()


def get_data(url: str):
    request = requests.get(url)
    request.raise_for_status()
    return request.content


def change_links_to_local(html: str, url: str, resources):
    resources_dir = utils.build_name(url, DIR_EXT)
    soup = BeautifulSoup(html, PARSER)
    tags = soup.find_all(resources)
    resources_urls = []
    for tag in tags:
        tag_link = get_link(tag)
        if not tag_link:
            continue
        if utils.is_same_netloc(url, tag_link):
            resources_urls.append(
                urljoin(
                    url if url.endswith('/') else '{0}/'.format(url),
                    get_link(tag),
                ),
            )
            change_tag_link(url, tag, resources_dir)
    return soup.prettify(formatter=FORMATTER), resources_urls


def get_link(tag) -> str:
    if tag.name == LINK:
        return tag.get(HREF, '')
    return tag.get(SRC, '')


def change_tag_link(url: str, tag, resources_dir: str):
    """Replace tag`s link with a local path."""
    resource_url = urljoin(url, get_link(tag))
    new_link = os.path.join(
        resources_dir,
        utils.build_name(resource_url),
    )
    if tag.name == LINK:
        tag[HREF] = new_link
    else:
        tag[SRC] = new_link


def write_to_file(path: str, dataset, mode: str):
    with open(path, mode) as data_file:
        data_file.write(dataset)


def make_dir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def save_resource(url: str, download_dir: str):
    file_path = os.path.join(download_dir, utils.build_name(url))
    dataset = get_data(url)
    mode = 'wb' if isinstance(dataset, bytes) else 'w'
    write_to_file(file_path, dataset, mode)
