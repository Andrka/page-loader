# -*- coding:utf-8 -*-

"""Realize command line interface."""

import argparse
import logging
import os

DEFAULT_PATH = os.getcwd()
LOGGING = {  # noqa: WPS407
    'full': logging.INFO,
    'short': logging.ERROR,
}


def parse_arguments():
    """Return parser of command line arguments."""
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument(
        '--output',
        default=DEFAULT_PATH,
        help='set save location (default: current directory)',
    )
    parser.add_argument(
        '--logging',
        default='full',
        choices=[
            'full',
            'short',
        ],
        help='set logging of output (default: full)',
    )
    parser.add_argument('url', help='set requested web page in full format')
    return parser
