# -*- coding: utf-8 -*-

from PySide2.QtCore import QSettings
from configparser import ConfigParser

from scihub_eva.globals.versions import *
from scihub_eva.utils.path_utils import *
from scihub_eva.utils.sys_utils import *


class Preferences(object):
    if is_macos():
        QSettings.setDefaultFormat(QSettings.Format.NativeFormat)
        SETTINGS = QSettings(QSettings.NativeFormat, QSettings.UserScope, ORGANIZATION_DOMAIN, APPLICATION_NAME)
    else:
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        SETTINGS = QSettings(QSettings.IniFormat, QSettings.UserScope, ORGANIZATION_DOMAIN, APPLICATION_NAME)

    def __init__(self):
        super(Preferences, self).__init__()

    @classmethod
    def contains(cls, key):
        return cls.SETTINGS.contains(key)

    @classmethod
    def get(cls, key, type=None):
        return cls.get_or_default(key, None, type=type)

    @classmethod
    def get_or_default(cls, key, default, type=None):
        if type is None:
            return cls.SETTINGS.value(key, default)
        else:
            return cls.SETTINGS.value(key, default, type=type)

    @classmethod
    def set(cls, key, value):
        cls.SETTINGS.setValue(key, value)

    @classmethod
    def remove(cls, key):
        cls.SETTINGS.remove(key)


class Config(ConfigParser):
    def __init__(self, config_file_path, space_around_delimiters=False):
        super(Config, self).__init__()

        self.optionxform = str
        self._config_file_path = config_file_path
        self.read(self._config_file_path)

        self._space_around_delimiters = space_around_delimiters

    def get_or_default(self, section, option, default_value):
        value = super(Config, self).get(section, option)
        return value if value else default_value

    def set(self, section, option, value=None):
        super(Config, self).set(section, option, value)
        self.save()

    def remove(self, section, option):
        super(Config, self).remove_option(section, option)
        self.save()

    def save(self):
        with open(self._config_file_path, 'w') as f:
            self.write(f, space_around_delimiters=self._space_around_delimiters)


QT_QUICK_CONTROLS2_CONFIG = Config((PREFERENCES_DIR / 'qtquickcontrols2.conf').resolve().as_posix())


def is_app_dark_theme():
    if QT_QUICK_CONTROLS2_CONFIG.get('Material', 'Theme') == 'Dark':
        return True
    elif QT_QUICK_CONTROLS2_CONFIG.get('Material', 'Theme') == 'Light':
        return False
    elif QT_QUICK_CONTROLS2_CONFIG.get('Material', 'Theme') == 'System':
        return is_system_dark_theme()
    else:
        return False


__all__ = [
    'Preferences',
    'Config',
    'QT_QUICK_CONTROLS2_CONFIG',
    'is_app_dark_theme'
]
