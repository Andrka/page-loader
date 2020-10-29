# -*- coding:utf-8 -*-

"""Realize command line interface."""

import argparse
import os

DEFAULT_PATH = os.getcwd()


def parse_arguments():
    """Return parser of command line arguments."""
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument(
        '--output',
        default=DEFAULT_PATH,
        help='set save location (default: current directory)',
    )
    parser.add_argument('url', help='set requested web page in full format')
    return parser
