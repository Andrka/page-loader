#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""General script."""

import sys

from page_loader import cli, engine, logging


def main():  # noqa: WPS213
    """Page loader."""
    args = cli.get_parser().parse_args()
    logging.set_logger(args.log)
    logger = logging.logging.getLogger('page_loader')
    try:
        engine.download(args.url, args.output)
    except engine.KnownError as exc:
        logger.debug(exc, exc_info=True)
        logger.error('Error: {0}'.format(exc))
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
