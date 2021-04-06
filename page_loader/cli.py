# -*- coding:utf-8 -*-

"""Realize command line interface."""

import argparse
import os

DEFAULT_PATH = os.getcwd()


def get_parser():
    """Return parser of command line arguments."""
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument(
        '-o',
        '--output',
        default=DEFAULT_PATH,
        help='set save location (default: current directory)',
    )
    parser.add_argument(
        '--log',
        default='info',
        choices=[
            'notset',
            'debug',
            'info',
            'warning',
            'error',
        ],
        help='set logging (default: info)',
    )
    parser.add_argument(
        'url',
        help='set requested web page in full format (with schema)',
    )
    return parser
