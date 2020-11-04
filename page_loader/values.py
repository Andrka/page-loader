# -*- coding:utf-8 -*-

"""Work with text argument values."""

import os
import re
from urllib.parse import urlparse

MAX_FILE_NAME_LENGTH = 255
FILE_NAME_END = '.html'
MAX_DIR_NAME_LENGTH = 4096
DIR_NAME_END = '_files'


def collect_path(
    output_path: str,
    url: str,
    output: str = 'file',
    extension: str = FILE_NAME_END,
) -> str:
    """Return saving path with given output path and file name (from url)."""
    parse_url = urlparse(url)
    network_path = parse_url.geturl()
    if parse_url.scheme:
        network_path = parse_url._replace(scheme='').geturl()  # noqa: WPS437
    saving_name = re.sub(r'\W', '-', re.sub(r'\/{2}', '', network_path))
    if output == 'dir':
        if len(saving_name) > MAX_DIR_NAME_LENGTH - len(DIR_NAME_END):
            saving_name = saving_name[:-len(DIR_NAME_END)]
        return '{0}{1}'.format(
            os.path.join(output_path, saving_name),
            DIR_NAME_END,
        )
    if len(saving_name) > MAX_FILE_NAME_LENGTH - len(extension):
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
    if tag.name in RESOURCES:
        if tag.has_attr(ATTR):
            url = urlparse(tag[ATTR])
            if not url.scheme and not url.netloc and url.path:
                return True
    return False
