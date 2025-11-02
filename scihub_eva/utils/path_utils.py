import os
from pathlib import Path

from scihub_eva.globals.versions import *
from scihub_eva.utils.sys_utils import *


def _logs_dir():
    if is_macos():
        logs_dir_path = (
            Path.home() / 'Library' / 'Logs/' / ORGANIZATION_DOMAIN / APPLICATION_NAME
        )
    elif is_windows():
        logs_dir_path = (
            Path.home()
            / 'AppData'
            / 'Local/'
            / ORGANIZATION_DOMAIN
            / APPLICATION_NAME
            / 'logs'
        )
    elif is_linux():
        logs_dir_path = (
            Path.home()
            / '.local'
            / 'share/'
            / ORGANIZATION_DOMAIN
            / APPLICATION_NAME
            / 'logs'
        )
    else:
        logs_dir_path = BASE_DIR / 'logs'

    if not logs_dir_path.exists():
        logs_dir_path.mkdir(parents=True)

    return logs_dir_path


BASE_DIR = Path(os.path.dirname(__file__)) / '../..'

CONFS_DIR = BASE_DIR / 'confs'
I18N_DIR = BASE_DIR / 'i18n'
IMAGES_DIR = BASE_DIR / 'images'
LOGS_DIR = _logs_dir()
UI_DIR = BASE_DIR / 'ui'


__all__ = ['BASE_DIR', 'CONFS_DIR', 'I18N_DIR', 'IMAGES_DIR', 'UI_DIR', 'LOGS_DIR']
