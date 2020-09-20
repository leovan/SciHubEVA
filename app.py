#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import locale

import scihubeva.resources

from PySide2.QtCore import Qt, QTranslator
from PySide2.QtGui import QGuiApplication, QIcon, QFont

from scihubeva.scihubeva_dialog import SciHubEVADialog
from scihubeva.utils import *

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


if __name__ == '__main__':
    app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.environ['QT_QUICK_CONTROLS_CONF'] = (CONF_DIR / 'qtquickcontrols2.conf').resolve().as_posix()

    app = QGuiApplication(sys.argv)

    lang = locale.getdefaultlocale()[0]
    lang_file_path = (TRANSLATION_DIR / 'SciHubEVA_{lang}.qm'.format(lang=lang)).resolve().as_posix()
    translator = QTranslator()
    translator.load(lang_file_path)
    app.installTranslator(translator)

    icon_file_path = (IMAGES_DIR / 'SciHubEVA-icon.png').resolve().as_posix()
    app.setWindowIcon(QIcon(icon_file_path))

    if is_windows():
        app.setFont(QFont('Microsoft YaHei'))

    eva = SciHubEVADialog()
    sys.exit(app.exec_())
