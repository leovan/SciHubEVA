# -*- coding: utf-8 -*-

import logging

from logging.handlers import TimedRotatingFileHandler

from scihub_eva.utils.path_utils import *


DEFAULT_LOGGER = logging.getLogger('default')
DEFAULT_LOGGER.setLevel(logging.INFO)

DEFAULT_LOG_DIRECTORY = LOGS_DIR
DEFAULT_LOG_FILE = DEFAULT_LOG_DIRECTORY / 'SciHubEVA.log'
DEFAULT_LOG_HANDLER = TimedRotatingFileHandler(
    DEFAULT_LOG_FILE.resolve().as_posix(), when='d', encoding='utf-8')
DEFAULT_LOG_HANDLER.setLevel(logging.INFO)

DEFAULT_LOG_FORMATTER = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')
DEFAULT_LOG_HANDLER.setFormatter(DEFAULT_LOG_FORMATTER)

DEFAULT_LOGGER.addHandler(DEFAULT_LOG_HANDLER)

LOGGER_SEP = '–' * 30


def format_log_message(message):
    return DEFAULT_LOG_FORMATTER.format(message)


__all__ = [
    'DEFAULT_LOG_DIRECTORY',
    'DEFAULT_LOG_FILE',
    'DEFAULT_LOG_HANDLER',
    'DEFAULT_LOG_FORMATTER',
    'DEFAULT_LOGGER',
    'LOGGER_SEP'
]
