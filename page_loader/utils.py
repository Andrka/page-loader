# -*- coding:utf-8 -*-

"""Work with paths and urls values."""

import os
import re
from urllib.parse import urljoin, urlparse, urlsplit

from bs4 import BeautifulSoup

LINK = 'link'
HREF = 'href'
SRC = 'src'
FILE_EXT = '.html'
DIR_EXT = '_files'
PARSER = 'html.parser'
FORMATTER = 'html5'
NON_LETTERS_AND_DIGITS = '[^A-Za-z0-9]+'
SYMBOL = '-'


def collect_file_name(url: str) -> str:
    """Generate file name from the url."""
    parse_url = urlsplit(url)
    url_without_schema = '{0}{1}'.format(parse_url.netloc, parse_url.path)
    if not parse_url.path:
        return '{0}{1}'.format(replace_symbols(url_without_schema), FILE_EXT)
    root, ext = os.path.splitext(url_without_schema)
    file_name = replace_symbols(root)
    if not ext:
        ext = FILE_EXT
    return '{0}{1}'.format(file_name, ext)


def replace_symbols(string: str) -> str:
    """Replace all characters in string with a hyphen."""
    return re.sub(NON_LETTERS_AND_DIGITS, SYMBOL, string)


def change_links_to_local(  # noqa: WPS210
    html: str,
    url: str,
    resources,
) -> str:
    """Change links to local paths.

    Change in given html resources links to local paths,
    and return changed html string with list of resources urls.

    """
    resources_dir = collect_dir_name(url)
    soup = BeautifulSoup(html, PARSER)
    tags = soup.find_all(resources)
    resources_urls = []
    for tag in tags:
        link = get_link(tag)
        if not link:
            continue
        if is_local_link(url, link):
            resources_urls.append(
                urljoin(
                    url if url.endswith('/') else '{0}/'.format(url),
                    get_link(tag),
                ),
            )
            change_tag_link(url, tag, resources_dir)
    return soup.prettify(formatter=FORMATTER), resources_urls


def is_local_link(url: str, link: str) -> bool:
    """Check if tag has a local link."""
    parse_url = urlparse(url)
    parse_link = urlparse(urljoin(url, link))
    if not parse_link.netloc:
        return True
    return parse_url.netloc == parse_link.netloc


def get_link(tag) -> str:
    """Return a link to resource."""
    if tag.name == LINK:
        return tag.get(HREF, '')
    return tag.get(SRC, '')


def collect_dir_name(url: str) -> str:
    """Generate directory name from the url."""
    return '{0}{1}'.format(
        os.path.splitext(collect_file_name(url))[0],
        DIR_EXT,
    )


def change_tag_link(url: str, tag, resources_dir: str):
    """Replace tag`s link with a local path."""
    resource_url = urljoin(url, get_link(tag))
    new_link = os.path.join(resources_dir, collect_file_name(resource_url))
    if tag.name == LINK:
        tag[HREF] = new_link
    else:
        tag[SRC] = new_link
