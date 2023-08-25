# -*- coding: utf-8 -*-

import os
import darkdetect

from scihub_eva.globals.preferences import *
from scihub_eva.utils.sys_utils import *
from scihub_eva.utils.path_utils import *
from scihub_eva.utils.preferences_utils import *


def center_window(window, parent_window):
    parent_window_center_x = parent_window.x() + int(parent_window.width() / 2)
    parent_window_center_y = parent_window.y() + int(parent_window.height() / 2)

    window_x = parent_window_center_x - int(window.width() / 2)
    window_y = parent_window_center_y - int(window.height() / 2)

    window.setPosition(window_x, window_y)


def is_system_dark_theme():
    return darkdetect.isDark() or False


def is_app_dark_theme():
    if os.environ['QT_QUICK_CONTROLS_MATERIAL_THEME'] == 'Dark':
        return True
    elif os.environ['QT_QUICK_CONTROLS_MATERIAL_THEME'] == 'Light':
        return False
    elif os.environ['QT_QUICK_CONTROLS_MATERIAL_THEME'] == 'System':
        return is_system_dark_theme()
    else:
        return False


def set_ui_env():
    qtquickcontrols2_conf_path = CONFS_DIR / 'qtquickcontrols2.conf'
    if qtquickcontrols2_conf_path.resolve().exists():
        os.environ['QT_QUICK_CONTROLS_CONF'] = \
            qtquickcontrols2_conf_path.resolve().as_posix()

    os.environ['QT_QUICK_CONTROLS_MATERIAL_THEME'] = \
        Preferences.get_or_default(SYSTEM_THEME_KEY, SYSTEM_THEME_DEFAULT)

    if is_app_dark_theme():
        os.environ['QT_QUICK_CONTROLS_MATERIAL_BACKGROUND'] = '#3F3F3F'
    else:
        os.environ['QT_QUICK_CONTROLS_MATERIAL_BACKGROUND'] = '#FFFFFF'

    if is_windows():
        os.environ['QSG_RHI_BACKEND'] = 'opengl'

    if is_linux():
        os.environ['GDK_BACKEND'] = 'x11'
        os.environ['QT_QPA_PLATFORM'] = 'xcb'

    os.environ['QT_ENABLE_GLYPH_CACHE_WORKAROUND'] = '1'
    os.environ['QML_USE_GLYPHCACHE_WORKAROUND'] = '1'


__all__ = [
    'center_window',
    'is_system_dark_theme',
    'is_app_dark_theme',
    'set_ui_env'
]
