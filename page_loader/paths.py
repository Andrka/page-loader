# -*- coding:utf-8 -*-

"""Work with paths and urls values."""

import os
import re
from urllib.parse import urlparse

MAX_NAME_LEN = 255
FILE_EXT = '.html'
MAX_DIR_LEN = 4096
DIR_EXT = '_files'
RESOURCES = ('link', 'script', 'img')
ATTR = 'src'


def url_to_path(
    output_path: str,
    url: str,
    output: str = 'file',
    extension: str = FILE_EXT,
) -> str:
    """Return saving path with given output path and file name (from url)."""
    parsing_url = urlparse(url)
    network_path = parsing_url.geturl()
    if parsing_url.scheme:
        network_path = parsing_url._replace(scheme='').geturl()  # noqa: WPS437
    saving_name = re.sub(r'\W', '-', re.sub(r'\/{2}', '', network_path))
    if output == 'dir':
        if len(saving_name) > MAX_DIR_LEN - len(DIR_EXT):
            saving_name = saving_name[:-len(DIR_EXT)]
        return '{0}{1}'.format(
            os.path.join(output_path, saving_name),
            DIR_EXT,
        )
    if len(saving_name) > MAX_NAME_LEN - len(extension):
        saving_name = saving_name[:-len(extension)]
    return '{0}{1}'.format(os.path.join(output_path, saving_name), extension)


def is_correct(url: str) -> bool:
    """Check correctness of url."""
    parsing_url = urlparse(url)
    if parsing_url.netloc:
        return True
    return False


def is_local_asset(tag) -> bool:
    """Check if given BeautifulSoup tag represents a local asset."""
    if tag.name not in RESOURCES or not tag.has_attr(ATTR):
        return False
    url = urlparse(tag[ATTR])
    return url.path and not url.scheme and not url.netloc
