# -*- coding: utf-8 -*-

import os
import sys

import scihub_eva.resources

from PySide6.QtCore import QCoreApplication, QTranslator
from PySide6.QtGui import QGuiApplication, QIcon

from scihub_eva.globals.versions import *
from scihub_eva.globals.preferences import *
from scihub_eva.utils.preferences_utils import *
from scihub_eva.utils.sys_utils import *
from scihub_eva.utils.path_utils import *
from scihub_eva.ui.scihub_eva import UISciHubEVA


if __name__ == '__main__':
    app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.environ['QT_QUICK_CONTROLS_CONF'] = (PREFERENCES_DIR / 'qtquickcontrols2.conf').resolve().as_posix()

    if is_windows():
        os.environ['QSG_RHI_BACKEND'] = 'opengl'

    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = QGuiApplication(sys.argv)

    lang = Preferences.get_or_default(SYSTEM_LANGUAGE_KEY, SYSTEM_LANGUAGE)
    lang_file_path = (I18N_DIR / 'SciHubEVA_{lang}.qm'.format(lang=lang)).resolve().as_posix()

    if os.path.exists(lang_file_path):
        translator = QTranslator()
        translator.load(lang_file_path)
        app.installTranslator(translator)

    icon_file_path = (IMAGES_DIR / 'SciHubEVA-icon.png').resolve().as_posix()
    app.setWindowIcon(QIcon(icon_file_path))

    eva = UISciHubEVA()
    sys.exit(app.exec())
