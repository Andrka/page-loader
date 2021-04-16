# -*- coding:utf-8 -*-

"""Work with file/dir names and links values."""

import os
import re
from urllib.parse import urljoin, urlparse, urlsplit

FILE_EXT = '.html'
DIR_EXT = '_files'
NON_LETTERS_AND_DIGITS = '[^A-Za-z0-9]+'
SYMBOL = '-'


def collect_file_name(url: str) -> str:
    """Generate file name from the url."""
    parse_url = urlsplit(url)
    url_without_schema = '{0}{1}'.format(parse_url.netloc, parse_url.path)
    if not parse_url.path:
        return '{0}{1}'.format(
            re.sub(NON_LETTERS_AND_DIGITS, SYMBOL, url_without_schema),
            FILE_EXT,
        )
    root, ext = os.path.splitext(url_without_schema)
    file_name = re.sub(NON_LETTERS_AND_DIGITS, SYMBOL, root)
    if not ext:
        ext = FILE_EXT
    return '{0}{1}'.format(file_name, ext)


def collect_dir_name(url: str) -> str:
    """Generate directory name from the url."""
    return '{0}{1}'.format(
        os.path.splitext(collect_file_name(url))[0],
        DIR_EXT,
    )


def is_local_link(url: str, link: str) -> bool:
    """Check if tag has a local link."""
    parse_url = urlparse(url)
    parse_link = urlparse(urljoin(url, link))
    if not parse_link.netloc:
        return True
    return parse_url.netloc == parse_link.netloc
