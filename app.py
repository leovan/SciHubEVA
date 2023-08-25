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
from scihub_eva.utils.ui_utils import *
from scihub_eva.ui.scihub_eva import UISciHubEVA


def main():
    multiprocessing.freeze_support()

    set_ui_env()

    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = QGuiApplication(sys.argv)

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
