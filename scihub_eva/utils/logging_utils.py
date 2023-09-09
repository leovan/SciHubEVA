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


class UISciHubEVALogHandler(logging.StreamHandler):
    def __init__(self, ui_scihub_eva):
        super(UISciHubEVALogHandler, self).__init__()

        self.formatter = DEFAULT_LOG_FORMATTER
        self._ui_scihub_eva = ui_scihub_eva

    def emit(self, record):
        message = self.format(record)
        self._ui_scihub_eva.append_log.emit(message)


__all__ = [
    'DEFAULT_LOG_DIRECTORY',
    'DEFAULT_LOG_FILE',
    'DEFAULT_LOG_HANDLER',
    'DEFAULT_LOG_FORMATTER',
    'DEFAULT_LOGGER',
    'LOGGER_SEP',
    'UISciHubEVALogHandler'
]
