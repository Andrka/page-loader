# -*- coding:utf-8 -*-

"""Download and save data module."""

import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from page_loader import values

STATUS_CODES = (200, )


def load(url: str):
    """Downdoad requested url and return Response object.

    Raises:
        ValueError: Can't find the page you're looking for.
    """
    page = requests.get(url)
    if page.status_code in STATUS_CODES:
        return page
    raise ValueError("Can't find the page you're looking for!")


def parse_html(path: str):
    """Parse given html file to BeautifulSoup object."""
    with open(path) as html:
        return BeautifulSoup(html, 'html.parser')


def save_html(output: str, load_data):
    """Save given Response object in html to output path."""
    with open(output, 'w') as output_file:
        output_file.write(load_data.text)


def save_data(output: str, load_data):
    """Save given data from Response object to output path."""
    with open(output, 'wb') as output_file:
        output_file.write(load_data.content)


def save_soup(output: str, soup):
    """Save BeautifulSoup object to output path."""
    with open(output, 'wb') as output_file:
        output_file.write(soup.encode('utf-8'))


def save(output: str, url: str):  # noqa: WPS210, WPS231
    """Save requested html file with resources to given path."""
    load_data = load(url)
    html_path = values.collect_path(output, url)
    if not os.path.isdir(output):
        os.mkdir(output)
    save_html(html_path, load_data)
    soup = parse_html(html_path)
    output_dir = values.collect_path(output, url, 'dir')
    os.mkdir(output_dir)
    resources = soup.find_all(values.is_resource)
    if url[-1] != '/':
        url = '{0}/'.format(url)
    for resource in resources:
        resource_url = urljoin(url, resource[values.ATTR])
        try:
            load_data = load(resource_url)
        except:  # noqa: S110, E722
            del resource[values.ATTR]  # noqa: WPS420
        else:
            resource_path, extension = os.path.splitext(resource[values.ATTR])
            data_path = values.collect_path(
                output_dir,
                resource_path,
                'file',
                extension,
            )
            save_data(data_path, load_data)
            _, resource_name = os.path.split(data_path)
            resource[values.ATTR] = os.path.join(
                os.path.basename(os.path.normpath(output_dir)),
                resource_name,
            )
            save_soup(html_path, soup)
