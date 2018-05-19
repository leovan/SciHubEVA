#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import locale
import os

from PyQt5.QtCore import QObject, Qt, QTranslator, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QGuiApplication, QIcon, QFont
from PyQt5.QtQml import QQmlApplicationEngine

from scihub_conf import SciHubConf
from scihub_preferences import SciHubPreferences
from scihub_api import SciHubAPI

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

try:
    import scihub_resources
except:
    pass

class SciHubEVA(QObject):
    beforeRampage = pyqtSignal()
    afterRampage = pyqtSignal()

    showErrorMessage = pyqtSignal(str, str)
    showInfoMessage = pyqtSignal(str, str)

    setSaveToDir = pyqtSignal(str)
    appendLogs = pyqtSignal(str)

    def __init__(self):
        super(SciHubEVA, self).__init__()

        self._conf = SciHubConf()

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/SciHubEVA.qml')
        self._window = self._engine.rootObjects()[0]
        self._connect()

        self._scihub_preferences = SciHubPreferences(self._conf)

        save_to_dir = self._conf.get('common', 'save_to_dir')
        if not save_to_dir or save_to_dir.strip() == '':
            self._save_to_dir = None
        else:
            self._save_to_dir = save_to_dir
            self.setSaveToDir.emit(save_to_dir)

    def _connect(self):
        # Connect QML signals to PyQt slots
        self._window.saveToDir.connect(self.saveToDir)
        self._window.rampage.connect(self.rampage)
        self._window.showWindowPreference.connect(self.showWindowPreferences)

        # Connect PyQt signals to QML slots
        self.beforeRampage.connect(self._window.beforeRampage)
        self.afterRampage.connect(self._window.afterRampage)

        self.showErrorMessage.connect(self._window.showErrorMessage)
        self.showInfoMessage.connect(self._window.showInfoMessage)

        self.setSaveToDir.connect(self._window.setSaveToDir)
        self.appendLogs.connect(self._window.appendLogs)

    @property
    def conf(self):
        return self._conf

    @pyqtSlot(str)
    def saveToDir(self, directory):
        self._save_to_dir = directory
        self._conf.set('common', 'save_to_dir', directory)

    @pyqtSlot()
    def showWindowPreferences(self):
        self._scihub_preferences.loadFromConf()
        self._scihub_preferences.showWindowPreferences.emit()

    @pyqtSlot(str)
    def rampage(self, query):
        scihub_api = SciHubAPI(query, callback=self._afterRampage, conf=self._conf, log=self._log)
        self._beforeRampage()
        scihub_api.start()

    def _beforeRampage(self):
        self.beforeRampage.emit()

    def _afterRampage(self):
        self.afterRampage.emit()

    def _log(self, message, type = None):
        if type:
            log_formater = '[{type}] - {message}'
        else:
            log_formater = '{message}'

        self.appendLogs.emit(log_formater.format(type=type, message=message))


if __name__ == '__main__':
    sys.argv += ['--style', 'material']
    app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    app = QGuiApplication(sys.argv)

    lang = locale.getdefaultlocale()[0]
    lang_file_path = os.path.join(app_path, 'translations/SciHubEVA_{lang}.qm'.format(lang=lang))
    translator = QTranslator()
    translator.load(lang_file_path)
    app.installTranslator(translator)

    icon_file_path = os.path.join(app_path, 'images/SciHubEVA.png')
    app.setWindowIcon(QIcon(icon_file_path))

    if sys.platform == 'win32':
        app.setFont(QFont('Microsoft YaHei'))

    eva = SciHubEVA()
    sys.exit(app.exec_())
