#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import locale
import os
import PySide2

from collections import deque
from pathlib import Path

from PySide2.QtCore import QObject, Qt, QTranslator, Slot, Signal
from PySide2.QtGui import QGuiApplication, QIcon, QFont
from PySide2.QtQml import QQmlApplicationEngine

from scihub_conf import SciHubConf
from scihub_preferences import SciHubPreferences
from scihub_captcha import SciHubCaptcha
from scihub_api import SciHubAPI, SciHubRampageType, SciHubError
from scihub_utils import show_directory, is_text_file, is_range_query, gen_range_query_list

import scihub_resources

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class SciHubEVA(QObject):
    beforeRampage = Signal()
    afterRampage = Signal()

    loadSaveToDir = Signal(str)
    appendLogs = Signal(str, str)

    def __init__(self):
        super(SciHubEVA, self).__init__()

        self._conf = SciHubConf('SciHubEVA.conf')
        self._qt_quick_controls2_conf = SciHubConf('qtquickcontrols2.conf', space_around_delimiters=False)

        self._engine = QQmlApplicationEngine()
        self._engine.rootContext().setContextProperty('PYTHON_VERSION', '.'.join(str(v) for v in sys.version_info[:3]))
        self._engine.rootContext().setContextProperty('QT_VERSION', PySide2.QtCore.qVersion())
        self._engine.load('qrc:/ui/SciHubEVA.qml')
        self._window = self._engine.rootObjects()[0]
        self._connect()

        self._scihub_preferences = SciHubPreferences(self._conf, self._qt_quick_controls2_conf)
        self._scihub_captcha = SciHubCaptcha(self, log=self.log)
        self._captcha_query = None

        self._input = None
        save_to_dir = self._conf.get('common', 'save_to_dir')
        if not save_to_dir or save_to_dir.strip() == '':
            self._save_to_dir = None
        else:
            self._save_to_dir = save_to_dir
            self.loadSaveToDir.emit(save_to_dir)

        self._query_list = None
        self._query_list_length = 0

        self._captcha_img_file_path = None

    def _connect(self):
        # Connect QML signals to PyQt slots
        self._window.setSaveToDir.connect(self.setSaveToDir)
        self._window.showSaveToDir.connect(self.showSaveToDir)
        self._window.rampage.connect(self.rampage)
        self._window.showWindowPreference.connect(self.showWindowPreference)

        # Connect PyQt signals to QML slots
        self.beforeRampage.connect(self._window.beforeRampage)
        self.afterRampage.connect(self._window.afterRampage)

        self.loadSaveToDir.connect(self._window.loadSaveToDir)
        self.appendLogs.connect(self._window.appendLogs)

    @property
    def conf(self):
        return self._conf

    @Slot(str)
    def setSaveToDir(self, directory):
        self._save_to_dir = directory
        self._conf.set('common', 'save_to_dir', directory)

    @Slot(str)
    def showSaveToDir(self, directory):
        if os.path.exists(directory):
            show_directory(directory)

    @Slot()
    def showWindowPreference(self):
        self._scihub_preferences.load_from_conf()
        self._scihub_preferences.showWindowPreferences.emit()

    @Slot(str)
    def rampage(self, input):
        """Download PDF with input

        Args:
            input: query or query list file path

        """

        self._input = input

        if os.path.exists(input):
            if is_text_file(input):
                self._query_list = deque()

                with open(input, 'rt') as f:
                    for line in f:
                        cleaned_line = line.strip()
                        if cleaned_line != '':
                            self._query_list.append(cleaned_line)

                self._query_list_length = len(self._query_list)
                self.rampage_query_list()
            else:
                self.log('<hr/>')
                self.log(self.tr('Query list file is not a text file!'), 'ERROR')
        elif is_range_query(input):
            self._query_list = deque(gen_range_query_list(input))
            self._query_list_length = len(self._query_list)
            self.rampage_query_list()
        else:
            self.rampage_query(input)


    def rampage_query_list(self):
        """Download PDF with query list (self._query_list)

        """

        if self._query_list and len(self._query_list) > 0:
            self.log('<hr/>')
            self.log(self.tr('Dealing with {}/{} query ...').format(
                self._query_list_length - len(self._query_list) + 1, self._query_list_length))

            self.rampage_query(self._query_list.popleft())

    def rampage_query(self, query):
        """Download PDF with query

        Args:
            query: Query of input

        """

        scihub_api = SciHubAPI(self._input, query, callback=self.rampage_callback,
                               rampage_type=SciHubRampageType.INPUT,
                               conf=self._conf, log=self.log)
        self.beforeRampage.emit()
        scihub_api.start()

    def rampage_with_captcha(self, captcha_answer):
        """ Download PDF with captcha query (self._captcha_query) and captcha answer

        Args:
            captcha_answer: Captcha answer

        """

        if os.path.exists(self._captcha_img_file_path) and os.path.isfile(self._captcha_img_file_path):
            os.remove(self._captcha_img_file_path)

        scihub_api = SciHubAPI(self._input, self._captcha_query, callback=self.rampage_callback,
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
            self.show_captcha(res)
        elif self._query_list:
            self.rampage_query_list()
        else:
            self.afterRampage.emit()

    def show_captcha(self, pdf_captcha_response):
        """Callback function for PDF captcha response

        Args:
            pdf_captcha_response: PDF captcha response

        """

        self._captcha_query = pdf_captcha_response

        scihub_api = SciHubAPI(self._input, None, log=self.log, conf=self._conf)
        _, captcha_img_url = scihub_api.get_captcha_info(pdf_captcha_response)
        captcha_img_file = scihub_api.download_captcha_img(captcha_img_url)
        self._captcha_img_file_path = Path(captcha_img_file.name).as_posix()
        captcha_img_local_uri = Path(captcha_img_file.name).as_uri()

        self._scihub_captcha.showWindowCaptcha.emit(captcha_img_local_uri)

    def log(self, message, level=None):
        self.appendLogs.emit(message, level)


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
