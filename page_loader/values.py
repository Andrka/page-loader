# -*- coding:utf-8 -*-

"""Work with text argument values."""

import os
import re
from urllib.parse import urlparse

MAX_NAME_LEN = 255
FILE_EXT = '.html'
MAX_DIR_LEN = 4096
DIR_EXT = '_files'


def collect(
    output_path: str,
    url: str,
    output: str = 'file',
    extension: str = FILE_EXT,
) -> str:
    """Return saving path with given output path and file name (from url)."""
    parse_url = urlparse(url)
    network_path = parse_url.geturl()
    if parse_url.scheme:
        network_path = parse_url._replace(scheme='').geturl()  # noqa: WPS437
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
    parse_url = urlparse(url)
    if parse_url.netloc:
        return True
    return False


RESOURCES = ('link', 'script', 'img')
ATTR = 'src'


def is_resource(tag) -> bool:
    """Check if given tag in BeautifulSoup object has resource link."""
    if tag.name not in RESOURCES or not tag.has_attr(ATTR):
        return False
    url = urlparse(tag[ATTR])
    return url.path and not url.scheme and not url.netloc
