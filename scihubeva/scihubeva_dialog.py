#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import html2text
import PySide2

from collections import deque
from logging.handlers import TimedRotatingFileHandler

from PySide2.QtCore import QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine

from scihubeva.configuration import Configuration
from scihubeva.preferences_dialog import PreferencesDialog
from scihubeva.captcha_dialog import CaptchaDialog
from scihubeva.scihub_api import SciHubAPI, RampageType, Error
from scihubeva.utils import *


class SciHubEVADialog(QObject):
    beforeRampage = Signal()
    afterRampage = Signal()

    loadSaveToDir = Signal(str)
    appendLogs = Signal(str, str)

    def __init__(self):
        super(SciHubEVADialog, self).__init__()

        self._conf = Configuration((CONF_DIR / 'SciHubEVA.conf').resolve().as_posix())
        self._qt_quick_controls2_conf = Configuration(
            (CONF_DIR / 'qtquickcontrols2.conf').resolve().as_posix(), space_around_delimiters=False)

        self._engine = QQmlApplicationEngine()
        self._engine.rootContext().setContextProperty('PYTHON_VERSION', '.'.join(str(v) for v in sys.version_info[:3]))
        self._engine.rootContext().setContextProperty('QT_VERSION', PySide2.QtCore.qVersion())
        self._engine.load('qrc:/ui/App.qml')
        self._window = self._engine.rootObjects()[0]
        self._theme = self._window.property('theme')
        self._connect()

        self._scihub_preferences = PreferencesDialog(self._conf, self._qt_quick_controls2_conf)
        self._scihub_captcha = CaptchaDialog(self, log=self.log)
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

        self._logger = logging.getLogger('SciHubEVA')
        self._logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_file_name_prefix = str(get_log_directory() / 'SciHubEVA.log')
        handler = TimedRotatingFileHandler(filename=log_file_name_prefix, when='D')
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)

        self._logger.addHandler(handler)

        self._h2t = html2text.HTML2Text()
        self._h2t.ignore_links = True

    def _connect(self):
        # Connect QML signals to PyQt slots
        self._window.setSaveToDir.connect(self.setSaveToDir)
        self._window.openSaveToDir.connect(self.openSaveToDir)
        self._window.rampage.connect(self.rampage)
        self._window.showWindowPreference.connect(self.showWindowPreference)
        self._window.openLogFile.connect(self.openLogFile)
        self._window.openLogDirectory.connect(self.openLogDirectory)

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
    def openSaveToDir(self, directory):
        if os.path.exists(directory):
            open_directory(directory)

    @Slot()
    def showWindowPreference(self):
        self._scihub_preferences.load_from_conf()
        self._scihub_preferences.showWindowPreferences.emit()

    @Slot()
    def openLogFile(self):
        open_file(str(get_log_directory() / 'SciHubEVA.log'))

    @Slot()
    def openLogDirectory(self):
        open_directory(str(get_log_directory()))

    @Slot(str)
    def rampage(self, input):
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
                self.log(self.tr('Query list file is not a text file!'), logging.ERROR)
        elif is_range_query(input):
            self._query_list = deque(gen_range_query_list(input))
            self._query_list_length = len(self._query_list)
            self.rampage_query_list()
        else:
            self.rampage_query(input)

    def rampage_query_list(self):
        if self._query_list and len(self._query_list) > 0:
            self.log('<hr/>')
            self.log(self.tr('Dealing with {}/{} query ...').format(
                self._query_list_length - len(self._query_list) + 1, self._query_list_length))

            self.rampage_query(self._query_list.popleft())

    def rampage_query(self, query):
        scihub_api = SciHubAPI(self._input, query, callback=self.rampage_callback,
                               rampage_type=RampageType.ORIGINAL,
                               conf=self._conf, log=self.log)
        self.beforeRampage.emit()
        scihub_api.start()

    def rampage_with_typed_captcha(self, captcha_answer):
        self.remove_captcha_img()

        scihub_api = SciHubAPI(self._input, self._captcha_query, callback=self.rampage_callback,
                               rampage_type=RampageType.WITH_TYPED_CAPTCHA,
                               conf=self._conf, log=self.log, captcha_answer=captcha_answer)

        self.beforeRampage.emit()
        scihub_api.start()

    def rampage_callback(self, res, err):
        if err == Error.BLOCKED_BY_CAPTCHA:
            self.show_captcha(res)
        elif self._query_list:
            self.rampage_query_list()
        else:
            self.afterRampage.emit()

    def show_captcha(self, pdf_captcha_response):
        self._captcha_query = pdf_captcha_response

        scihub_api = SciHubAPI(self._input, None, log=self.log, conf=self._conf)
        _, captcha_img_url = scihub_api.get_captcha_info(pdf_captcha_response)
        invert_color = True if self._theme == 1 else False
        captcha_img_file_path = scihub_api.download_captcha_img(captcha_img_url, invert_color=invert_color)
        self._captcha_img_file_path = captcha_img_file_path.resolve().as_posix()
        captcha_img_local_uri = captcha_img_file_path.as_uri()

        self._scihub_captcha.showWindowCaptcha.emit(captcha_img_local_uri)

    def remove_captcha_img(self):
        if os.path.exists(self._captcha_img_file_path) and os.path.isfile(self._captcha_img_file_path):
            os.remove(self._captcha_img_file_path)

    def log(self, message: str, level=None):
        self.appendLogs.emit(message, logging.getLevelName(level) if level else '')

        text_message = self._h2t.handle(message).strip()
        if text_message and text_message != '':
            self._logger.log(level if level else logging.INFO, text_message)
