# -*- coding:utf-8 -*-

"""Logging settings."""

import logging

FORMAT = '%(levelname)s - %(asctime)s - %(message)s'  # noqa: WPS323
DATEFMT = '%d-%b-%y %H:%M:%S'  # noqa: WPS323


def set_logger(log_level: str):
    """Set logger."""
    logger = logging.getLogger('page_loader')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(FORMAT, DATEFMT)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    if log_level == 'debug':
        logger.setLevel(level=logging.DEBUG)
    elif log_level == 'info':
        logger.setLevel(level=logging.INFO)
    elif log_level == 'warning':
        logger.setLevel(level=logging.WARNING)
    elif log_level == 'error':
        logger.setLevel(level=logging.ERROR)
    else:
        logger.setLevel(level=logging.NOTSET)
