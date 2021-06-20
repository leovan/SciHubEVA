# -*- coding: utf-8 -*-

import os

from collections import deque
from logging import StreamHandler

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtQml import QQmlApplicationEngine

from scihub_eva.globals.versions import *
from scihub_eva.globals.preferences import *
from scihub_eva.utils.sys_utils import *
from scihub_eva.utils.logging_utils import *
from scihub_eva.utils.preferences_utils import *
from scihub_eva.utils.ui_utils import *
from scihub_eva.utils.api_utils import *
from scihub_eva.api.scihub_api import *
from scihub_eva.ui.preferences import UIPreferences
from scihub_eva.ui.captcha import UICaptcha


class UISciHubEVALogHandler(StreamHandler):
    def __init__(self, ui_scihub_eva):
        super(UISciHubEVALogHandler, self).__init__()

        self.formatter = DEFAULT_LOG_FORMATTER
        self._ui_scihub_eva = ui_scihub_eva

    def emit(self, record):
        message = self.format(record)
        self._ui_scihub_eva.append_log.emit(message)


class UISciHubEVA(QObject):
    set_save_to_dir = Signal(str)
    append_log = Signal(str)
    before_rampage = Signal()
    after_rampage = Signal()

    def __init__(self):
        super(UISciHubEVA, self).__init__()

        self._engine = QQmlApplicationEngine()
        self._engine.rootContext().setContextProperty('APPLICATION_VERSION', APPLICATION_VERSION)
        self._engine.rootContext().setContextProperty('PYTHON_VERSION', PYTHON_VERSION)
        self._engine.rootContext().setContextProperty('QT_VERSION', QT_VERSION)
        self._engine.load('qrc:/ui/SciHubEVA.qml')
        self._window = self._engine.rootObjects()[0]

        self._logger = DEFAULT_LOGGER
        self._logger.addHandler(UISciHubEVALogHandler(self))

        self._connect()

        self._ui_preferences = UIPreferences(self)
        self._ui_captcha = UICaptcha(self, self._logger)
        self._captcha_query = None

        self._query_input = None
        self._query_list = None
        self._query_list_length = 0
        self._captcha_img_file_path = None

        self._save_to_dir = Preferences.get_or_default(FILE_SAVE_TO_DIR_KEY, FILE_SAVE_TO_DIR_DEFAULT)
        self.set_save_to_dir.emit(self._save_to_dir)

    @property
    def window(self):
        return self._window

    def _connect(self):
        self._window.openSaveToDir.connect(self.open_save_to_dir)
        self._window.systemOpenSaveToDir.connect(self.system_open_save_to_dir)
        self._window.showUIPreference.connect(self.show_ui_preference)
        self._window.systemOpenLogFile.connect(self.system_open_log_file)
        self._window.systemOpenLogDirectory.connect(self.system_open_log_directory)
        self._window.rampage.connect(self.rampage)

        self.set_save_to_dir.connect(self._window.setSaveToDir)
        self.append_log.connect(self._window.appendLog)
        self.before_rampage.connect(self._window.beforeRampage)
        self.after_rampage.connect(self._window.afterRampage)

    @Slot(str)
    def open_save_to_dir(self, directory):
        self._save_to_dir = directory
        Preferences.set(FILE_SAVE_TO_DIR_KEY, directory)

    @Slot(str)
    def system_open_save_to_dir(self, directory):
        if os.path.exists(directory):
            open_directory(directory)

    @Slot()
    def show_ui_preference(self):
        self._ui_preferences.load_preferences()
        center_window(self._ui_preferences.window, self._window)
        self._ui_preferences.show.emit()

    @Slot()
    def system_open_log_file(self):
        open_file(DEFAULT_LOG_FILE)

    @Slot()
    def system_open_log_directory(self):
        open_directory(DEFAULT_LOG_DIRECTORY)

    @Slot(str)
    def rampage(self, query_input):
        self._query_input = query_input

        if os.path.exists(query_input):
            if is_text_file(query_input):
                self._query_list = deque()

                with open(query_input, 'rt') as f:
                    for line in f:
                        cleaned_line = line.strip()
                        if cleaned_line != '':
                            self._query_list.append(cleaned_line)

                self._query_list_length = len(self._query_list)
                self.rampage_query_list()
            else:
                self._logger.error(LOGGER_SEP)
                self._logger.error(self.tr('Query list file is not a text file!'))
        elif is_range_query(query_input):
            self._query_list = deque(gen_range_query_list(query_input))
            self._query_list_length = len(self._query_list)
            self.rampage_query_list()
        else:
            self.rampage_query(query_input)

    def rampage_query_list(self):
        if self._query_list and len(self._query_list) > 0:
            self._logger.info(LOGGER_SEP)
            self._logger.info(self.tr('Dealing with {}/{} query ...').format(
                self._query_list_length - len(self._query_list) + 1, self._query_list_length))

            self.rampage_query(self._query_list.popleft())

    def rampage_query(self, query):
        scihub_api = SciHubAPI(
            self._query_input,
            query,
            logger=self._logger,
            callback=self.rampage_callback,
            rampage_type=SciHubEVARampageType.ORIGINAL)
        self.before_rampage.emit()
        scihub_api.start()

    def rampage_with_typed_captcha(self, captcha_answer):
        self.remove_captcha_img()

        scihub_api = SciHubAPI(
            self._query_input,
            self._captcha_query,
            logger=self._logger,
            callback=self.rampage_callback,
            rampage_type=SciHubEVARampageType.WITH_TYPED_CAPTCHA,
            captcha_answer=captcha_answer)

        self.before_rampage.emit()
        scihub_api.start()

    def rampage_callback(self, res, err):
        if err == SciHubAPIError.BLOCKED_BY_CAPTCHA:
            self.show_captcha(res)
        elif self._query_list:
            self.rampage_query_list()
        else:
            self.after_rampage.emit()

    def show_captcha(self, pdf_captcha_response):
        self._captcha_query = pdf_captcha_response

        scihub_api = SciHubAPI(
            self._query_input,
            None,
            logger=self._logger)
        _, captcha_img_url = scihub_api.get_captcha_info(pdf_captcha_response)
        invert_color = True if is_app_dark_theme() == 1 else False
        captcha_img_file_path = scihub_api.download_captcha_img(captcha_img_url, invert_color=invert_color)
        self._captcha_img_file_path = captcha_img_file_path.resolve().as_posix()
        captcha_img_local_uri = captcha_img_file_path.as_uri()

        self._ui_captcha.show_ui_captcha.emit(captcha_img_local_uri)
        center_window(self._ui_captcha.window, self._window)

    def remove_captcha_img(self):
        if os.path.exists(self._captcha_img_file_path) and os.path.isfile(self._captcha_img_file_path):
            os.remove(self._captcha_img_file_path)
