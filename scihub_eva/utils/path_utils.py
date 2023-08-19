# -*- coding: utf-8 -*-

import os

from pathlib import Path

from scihub_eva.globals.versions import *
from scihub_eva.utils.sys_utils import *


BASE_DIR = Path(os.path.dirname(__file__)) / '../..'
PREFERENCES_DIR = BASE_DIR / 'preferences'
UI_DIR = BASE_DIR / 'ui'
I18N_DIR = BASE_DIR / 'i18n'
IMAGES_DIR = BASE_DIR / 'images'
LOCAL_LOGS_DIR = BASE_DIR / 'logs'


def logs_dir():
    if is_macos():
        logs_dir_path = Path.home() / 'Library' / 'Logs/' / ORGANIZATION_DOMAIN / APPLICATION_NAME
    elif is_windows():
        logs_dir_path = Path.home() / 'AppData' / 'Local/' / ORGANIZATION_DOMAIN / APPLICATION_NAME / 'logs'
    elif is_linux():
        logs_dir_path = Path.home() / '.local' / 'share/' / ORGANIZATION_DOMAIN / APPLICATION_NAME / 'logs'
    else:
        logs_dir_path = LOCAL_LOGS_DIR

    if not logs_dir_path.exists():
        logs_dir_path.mkdir(parents=True)

    return logs_dir_path


__all__ = [
    'BASE_DIR',
    'PREFERENCES_DIR',
    'UI_DIR',
    'I18N_DIR',
    'IMAGES_DIR',
    'LOCAL_LOGS_DIR',
    'logs_dir'
]
