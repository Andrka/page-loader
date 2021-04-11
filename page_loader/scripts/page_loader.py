#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""General script."""

import logging
import sys

import requests

from page_loader import cli, page

FORMAT = '%(levelname)s - %(asctime)s - %(message)s'  # noqa: WPS323


def main():  # noqa: WPS213
    """Page loader."""
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    logger = logging.getLogger('page_loader')
    args = cli.get_args()
    try:  # noqa: WPS225
        print(page.download(args.url, args.output))  # noqa: WPS421
    except requests.exceptions.MissingSchema as exc:
        logger.error('Wrong url: {0}'.format(exc))
        sys.exit(1)
    except FileNotFoundError as exc:
        logger.error('No such file or directory: {0}'.format(exc))
        sys.exit(1)
    except PermissionError as exc:
        logger.error('Permission error: {0}'.format(exc))
        sys.exit(1)
    except OSError as exc:
        logger.error('{0}'.format(exc))
        sys.exit(1)
    except requests.HTTPError as exc:
        logger.error('Connection error: {0}'.format(exc))
        sys.exit(1)


if __name__ == '__main__':
    main()
