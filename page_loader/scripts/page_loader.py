#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""General script."""

import sys

from page_loader import cli, files, log, values


def main():  # noqa: WPS213
    """Page loader."""
    args = cli.parse_arguments().parse_args()
    logger = log.set_logger(args.log)
    if not values.is_correct(args.url):
        logger.error('wrong url')
        sys.exit(1)
    try:
        files.save(args.output, args.url)
    except log.KnownError:
        sys.exit(1)
    logger.info('"{0}" was downloaded!'.format(args.url))
    sys.exit(0)


if __name__ == '__main__':
    main()
