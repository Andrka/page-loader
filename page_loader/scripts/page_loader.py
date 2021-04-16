#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""General script."""

import logging
import sys

import requests
from page_loader import cli, page

FORMAT = '%(levelname)s - %(asctime)s - %(message)s'


def main():
    """Page loader."""
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    logger = logging.getLogger('page_loader')
    args = cli.get_args()
    try:
        print(page.download(args.url, args.output))
    except (
        requests.exceptions.MissingSchema,
        FileNotFoundError,
        PermissionError,
        OSError,
        requests.HTTPError,
    ) as exc:
        logger.error('Error: {0}'.format(exc))
        sys.exit(1)


if __name__ == '__main__':
    main()
