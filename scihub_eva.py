#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import locale
import os

from PySide2.QtCore import QObject, Qt, QTranslator, Slot, Signal
from PySide2.QtGui import QGuiApplication, QIcon, QFont
from PySide2.QtQml import QQmlApplicationEngine

from scihub_conf import SciHubConf
from scihub_preferences import SciHubPreferences
from scihub_captcha import SciHubCaptcha
from scihub_api import SciHubAPI, SciHubRampageType, SciHubError

import scihub_resources

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class SciHubEVA(QObject):
    beforeRampage = Signal()
    afterRampage = Signal()

    setSaveToDir = Signal(str)
    appendLogs = Signal(str)

    def __init__(self):
        super(SciHubEVA, self).__init__()

        self._conf = SciHubConf('SciHubEVA.conf')
        self._qt_quick_controls2_conf = SciHubConf('qtquickcontrols2.conf', space_around_delimiters=False)

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/SciHubEVA.qml')
        self._window = self._engine.rootObjects()[0]
        self._connect()

        self._scihub_preferences = SciHubPreferences(self._conf, self._qt_quick_controls2_conf)
        self._scihub_captcha = SciHubCaptcha(self, log=self.log)
        self._captcha_query = None

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

        self.setSaveToDir.connect(self._window.setSaveToDir)
        self.appendLogs.connect(self._window.appendLogs)

    @property
    def conf(self):
        return self._conf

    @Slot(str)
    def saveToDir(self, directory):
        self._save_to_dir = directory
        self._conf.set('common', 'save_to_dir', directory)

    @Slot()
    def showWindowPreferences(self):
        self._scihub_preferences.loadFromConf()
        self._scihub_preferences.showWindowPreferences.emit()

    @Slot(str)
    def rampage(self, input_query):
        """Download PDF with query of input

        Args:
            input_query: Query of input

        """

        scihub_api = SciHubAPI(input_query, callback=self.rampage_callback,
                               rampage_type=SciHubRampageType.INPUT,
                               conf=self._conf, log=self.log)
        self.beforeRampage.emit()
        scihub_api.start()

    def rampageWithCaptchar(self, captcha_answer):
        """ Download PDF with captcha query (self._captcha_query) and captcha answer

        Args:
            captcha_answer: Captcha answer

        """

        scihub_api = SciHubAPI(self._captcha_query, callback=self.rampage_callback,
                               rampage_type=SciHubRampageType.PDF_CAPTCHA_RESPONSE,
                               conf=self._conf, log=self.log, captcha_answer=captcha_answer)

        self.beforeRampage.emit()
        scihub_api.start()

    def rampage_callback(self, res, err):
        """Callback function

        Args:
            res: Result from last round rampage
            err: Error

        """

        if err == SciHubError.BLOCKED_BY_CAPTCHA:
            self.captcha_callback(res)
        else:
            self.afterRampage.emit()

    def captcha_callback(self, pdf_captcha_response):
        """Callback function for PDF captcha response

        Args:
            pdf_captcha_response: PDF captcha response

        """

        self._captcha_query = pdf_captcha_response
        _, captcha_img_url = SciHubAPI.get_captcha_info(pdf_captcha_response)
        self._scihub_captcha.showWindowCaptcha.emit(captcha_img_url)

    def log(self, message, level=None):
        if level:
            log_formatter = '[{level}] - {message}'
        else:
            log_formatter = '{message}'

        self.appendLogs.emit(log_formatter.format(level=level, message=message))


if __name__ == '__main__':
    app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.environ['QT_QUICK_CONTROLS_CONF'] = os.path.join(app_path, 'qtquickcontrols2.conf')

    app = QGuiApplication(sys.argv)

    lang = locale.getdefaultlocale()[0]
    lang_file_path = os.path.join(app_path, 'translations/SciHubEVA_{lang}.qm'.format(lang=lang))
    translator = QTranslator()
    translator.load(lang_file_path)
    app.installTranslator(translator)

    icon_file_path = os.path.join(app_path, 'images/SciHubEVA-icon.png')
    app.setWindowIcon(QIcon(icon_file_path))

    if sys.platform == 'win32':
        app.setFont(QFont('Microsoft YaHei'))

    eva = SciHubEVA()
    sys.exit(app.exec_())
