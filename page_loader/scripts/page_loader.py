#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""General script."""

from page_loader import cli, files, values


def main():
    """Page loader.

    Raises:
        ValueError: Wrong url.
    """
    args = cli.parse_arguments().parse_args()
    if not values.is_correct(args.url):
        raise ValueError('Wrong url!')
    files.save(
        files.load(args.url),
        values.collect_path(args.output, args.url),
    )
    print('Done!')  # noqa: WPS421


if __name__ == '__main__':
    main()
