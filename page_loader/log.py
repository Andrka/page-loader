# -*- coding:utf-8 -*-

"""Logging and exception instances."""

import logging
import sys


class LogFilter(logging.Filter):
    """Filter for logging messages with set level."""

    def __init__(self, level):
        """Init class."""
        self.level = level

    def filter(self, record):  # noqa: WPS125
        """Filter based on record."""
        return record.levelno < self.level


FORMAT = '%(levelname)s - %(asctime)s - %(message)s'  # noqa: WPS323
DATEFMT = '%d-%b-%y %H:%M:%S'  # noqa: WPS323
FORMATTER = logging.Formatter(FORMAT, DATEFMT)
LOG_LEVELS = {  # noqa: WPS407
    'full': logging.INFO,
    'errors': logging.ERROR,
}


def set_logger(log_format: str):
    """Set and return logger splitting loglevels between stdout and stderr."""
    logging_out = logging.StreamHandler(sys.stdout)
    logging_err = logging.StreamHandler(sys.stderr)
    logging_out.setFormatter(FORMATTER)
    logging_err.setFormatter(FORMATTER)
    logging_out.addFilter(LogFilter(logging.WARNING))
    logging_out.setLevel(logging.DEBUG)
    logging_err.setLevel(logging.WARNING)
    logger = logging.getLogger()
    logger.addHandler(logging_out)
    logger.addHandler(logging_err)
    logger.setLevel(LOG_LEVELS[log_format])
    return logger
