# -*- coding:utf-8 -*-

"""Realize command line interface."""

import argparse
import os

DEFAULT_PATH = os.getcwd()


def get_args():
    """Return command line arguments."""
    parser = argparse.ArgumentParser(description="""'Page loader' is a written
    in Python utility which downloads requested web page with local
     resources.""")
    parser.add_argument(
        '-o',
        '--output',
        default=DEFAULT_PATH,
        help='set output path (default: current directory)',
    )
    parser.add_argument(
        'url',
        help='set requested web page in full format (with schema)',
    )
    return parser.parse_args()
