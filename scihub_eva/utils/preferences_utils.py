# -*- coding: utf-8 -*-

from PySide6.QtCore import QSettings

from scihub_eva.globals.versions import *
from scihub_eva.utils.sys_utils import *


class Preferences(object):
    if is_macos():
        QSettings.setDefaultFormat(QSettings.Format.NativeFormat)
        SETTINGS = QSettings(
            QSettings.NativeFormat,
            QSettings.UserScope,
            ORGANIZATION_DOMAIN,
            APPLICATION_NAME)
    else:
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        SETTINGS = QSettings(
            QSettings.IniFormat,
            QSettings.UserScope,
            ORGANIZATION_DOMAIN,
            APPLICATION_NAME)

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


__all__ = [
    'Preferences'
]
