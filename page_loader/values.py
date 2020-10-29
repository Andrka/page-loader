# -*- coding:utf-8 -*-

"""Work with text argument values."""

import os
import re
from urllib.parse import urlparse


def collect_path(output_path: str, url: str) -> str:
    """Form path with given output path and file name from url."""
    parse_url = urlparse(url)
    network_path = parse_url._replace(scheme='').geturl()[2:]  # noqa: WPS437
    file_name = re.sub(r'\W', '-', network_path)
    return '{0}.html'.format(os.path.join(output_path, file_name))


def is_correct(url: str) -> bool:
    """Check correctness of url."""
    parse_url = urlparse(url)
    if parse_url.scheme and parse_url.netloc:
        return True
    return False
