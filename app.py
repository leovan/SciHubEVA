# -*- coding: utf-8 -*-

import os
import sys
import multiprocessing

import scihub_eva.resources

from PySide6.QtCore import QCoreApplication, QTranslator
from PySide6.QtGui import QGuiApplication, QIcon

from scihub_eva.globals.versions import *
from scihub_eva.globals.preferences import *
from scihub_eva.utils.preferences_utils import *
from scihub_eva.utils.sys_utils import *
from scihub_eva.utils.path_utils import *
from scihub_eva.ui.scihub_eva import UISciHubEVA


def main():
    multiprocessing.freeze_support()

    app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.environ['QT_QUICK_CONTROLS_CONF'] = (
            PREFERENCES_DIR / 'qtquickcontrols2.conf').resolve().as_posix()

    if is_windows():
        os.environ['QSG_RHI_BACKEND'] = 'opengl'

    os.environ['QT_ENABLE_GLYPH_CACHE_WORKAROUND'] = '1'
    os.environ['QML_USE_GLYPHCACHE_WORKAROUND'] = '1'

    if is_app_dark_theme():
        os.environ['QT_QUICK_CONTROLS_MATERIAL_BACKGROUND'] = '#3F3F3F'
    else:
        os.environ['QT_QUICK_CONTROLS_MATERIAL_BACKGROUND'] = '#FFFFFF'

    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    argv = [app_path, '--ignore-gpu-blacklist', '--enable-gpu-rasterization']
    app = QGuiApplication(argv)

    lang = Preferences.get_or_default(SYSTEM_LANGUAGE_KEY, SYSTEM_LANGUAGE)
    lang_file_path = (I18N_DIR / 'SciHubEVA_{lang}.qm'.format(
        lang=lang)).resolve().as_posix()

    if os.path.exists(lang_file_path):
        translator = QTranslator()
        translator.load(lang_file_path)
        app.installTranslator(translator)

    icon_file_path = (IMAGES_DIR / 'SciHubEVA-icon.png').resolve().as_posix()
    app.setWindowIcon(QIcon(icon_file_path))

    UISciHubEVA()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
