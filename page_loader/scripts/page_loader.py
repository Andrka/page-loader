#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""General script."""

import sys

from page_loader import cli, engine, logging, paths


def main():  # noqa: WPS213
    """Page loader."""
    parser = cli.get_parser()
    args = parser.parse_args()
    logging.set_logger(args.log)
    logger = logging.logging.getLogger('page_loader')
    if not paths.is_correct(args.url):
        logger.error('wrong url')
        sys.exit(1)
    try:
        engine.download_page(args.output, args.url)
    except engine.KnownError as exc:
        logger.debug(exc, exc_info=True)
        logger.error('Eerror: {0}'.format(exc))
        sys.exit(1)
    logger.info('"{0}" was downloaded!'.format(args.url))
    sys.exit(0)


if __name__ == '__main__':
    main()
