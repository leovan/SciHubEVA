from typing import Any

from PySide6.QtCore import QSettings

from scihub_eva.globals.versions import *
from scihub_eva.utils.sys_utils import *


class Preferences(object):
    if is_macos():
        QSettings.setDefaultFormat(QSettings.Format.NativeFormat)
        SETTINGS = QSettings(
            QSettings.Format.NativeFormat,
            QSettings.Scope.UserScope,
            ORGANIZATION_DOMAIN,
            APPLICATION_NAME,
        )
    else:
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        SETTINGS = QSettings(
            QSettings.Format.IniFormat,
            QSettings.Scope.UserScope,
            ORGANIZATION_DOMAIN,
            APPLICATION_NAME,
        )

    def __init__(self) -> None:
        super(Preferences, self).__init__()

    @classmethod
    def contains(cls, key: str) -> bool:
        return cls.SETTINGS.contains(key)

    @classmethod
    def get(cls, key: str, value_type: type | None = None) -> Any:
        return cls.get_or_default(key, None, value_type=value_type)

    @classmethod
    def get_or_default(
        cls, key: str, default: Any, value_type: type | None = None
    ) -> Any:
        if value_type is None:
            return cls.SETTINGS.value(key, default)
        else:
            return cls.SETTINGS.value(key, default, type=value_type)

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        cls.SETTINGS.setValue(key, value)

    @classmethod
    def remove(cls, key: str) -> None:
        cls.SETTINGS.remove(key)


__all__ = ['Preferences']
