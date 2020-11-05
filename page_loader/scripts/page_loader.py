#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""General script."""

import logging

from page_loader import cli, files, values


def main():
    """Page loader.

    Raises:
        ValueError: Wrong url.
    """
    args = cli.parse_arguments().parse_args()
    logging.basicConfig(
        format='%(levelname)s - %(asctime)s - %(message)s',  # noqa: WPS323
        level=cli.LOGGING[args.logging],
        datefmt='%d-%b-%y %H:%M:%S',  # noqa: WPS323
    )
    if not values.is_correct(args.url):
        logging.critical('wrong url')
        raise ValueError('Wrong url!')
    files.save(args.output, args.url)
    logging.info('"{0}" was downloaded!'.format(args.url))


if __name__ == '__main__':
    main()
