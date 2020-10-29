# -*- coding:utf-8 -*-

"""Download and save data module."""

import requests

STATUS_CODES = (200, )


def load(url: str):
    """Downdoad requested url and return Response object.

    Raises:
        ValueError: Can't find the page that you're looking for.
    """
    page = requests.get(url)
    if page.status_code in STATUS_CODES:
        return page
    raise ValueError("Can't find the page that you're looking for!")


def save(load_data, output_path: str):
    """Save given Response object in html file to given path."""
    with open(output_path, 'w') as output_file:
        output_file.write(load_data.text)
