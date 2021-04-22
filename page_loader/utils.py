# -*- coding:utf-8 -*-

"""Work with file/dir names and links values."""

import os
import re
from urllib.parse import urljoin, urlparse

NON_LETTERS_AND_DIGITS = '[^A-Za-z0-9]+'
SYMBOL = '-'
FILE_EXT = '.html'


def build_name(url: str, name_end: str = FILE_EXT) -> str:
    """Build file or dir name from the url."""
    parse_url = urlparse(url)
    url_without_schema = '{0}{1}'.format(parse_url.netloc, parse_url.path)
    root, ext = os.path.splitext(url_without_schema)
    changed_name = re.sub(NON_LETTERS_AND_DIGITS, SYMBOL, root)
    return '{0}{1}'.format(changed_name, ext if ext else name_end)


def is_same_netloc(url: str, tag_link: str) -> bool:
    """Check if url and tag link have same netloc."""
    parse_url = urlparse(url)
    parse_link = urlparse(urljoin(url, tag_link))
    if not parse_link.netloc:
        return True
    return parse_url.netloc == parse_link.netloc
