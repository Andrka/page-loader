# -*- coding:utf-8 -*-

"""Work with file/dir names and links values."""

import os
import re
from urllib.parse import urljoin, urlparse

REPLACEMENT_PATTERN = '[^A-Za-z0-9]+'
REPLACER = '-'
HTML_FILE_EXT = '.html'


def build_name(
    url: str,
    postfix: str = HTML_FILE_EXT,
    replacement_pattern: str = REPLACEMENT_PATTERN,
    replacer: str = REPLACER,
) -> str:
    """Build file or dir name from the url."""
    parsed_url = urlparse(url)
    url_without_schema = '{0}{1}'.format(parsed_url.netloc, parsed_url.path)
    root, ext = os.path.splitext(url_without_schema)
    changed_name = re.sub(replacement_pattern, replacer, root)
    return '{0}{1}'.format(changed_name, ext if ext else postfix)


def is_same_netloc(url: str, tag_link: str) -> bool:
    """Check if url and tag link have same netloc."""
    parsed_url = urlparse(url)
    parsed_link = urlparse(urljoin(url, tag_link))
    if not parsed_link.netloc:
        return True
    return parsed_url.netloc == parsed_link.netloc
