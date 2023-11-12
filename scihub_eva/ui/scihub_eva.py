# -*- coding: utf-8 -*-

import os
import gc

from collections import deque

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtQml import QQmlApplicationEngine

from scihub_eva.globals.versions import *
from scihub_eva.globals.preferences import *
from scihub_eva.utils.sys_utils import *
from scihub_eva.utils.logging_utils import *
from scihub_eva.utils.preferences_utils import *
from scihub_eva.utils.network_utils import *
from scihub_eva.utils.ui_utils import *
from scihub_eva.utils.api_utils import *
from scihub_eva.api.scihub_api import *
from scihub_eva.ui.preferences import UIPreferences
from scihub_eva.ui.captcha import UICaptcha


class UISciHubEVA(QObject):
    set_save_to_dir = Signal(str)
    append_log = Signal(str)
    before_rampage = Signal()
    after_rampage = Signal()

    def __init__(self):
        super(UISciHubEVA, self).__init__()

        self._engine = QQmlApplicationEngine()
        self._engine.rootContext().setContextProperty(
            'APPLICATION_VERSION', APPLICATION_VERSION)
        self._engine.rootContext().setContextProperty(
            'PYTHON_VERSION', PYTHON_VERSION)
        self._engine.rootContext().setContextProperty(
            'QT_VERSION', QT_VERSION)
        self._engine.load('qrc:/ui/SciHubEVA.qml')
        self._window = self._engine.rootObjects()[0]

        self._logger = DEFAULT_LOGGER
        self._logger.addHandler(UISciHubEVALogHandler(self))

        self._connect()

        self._ui_preferences = UIPreferences(self)
        self._ui_captcha = UICaptcha(self, self._logger)

        self._query_list = None
        self._query_list_length = 0
        self._captcha_img_file_path = None

        self._save_to_dir = Preferences.get_or_default(
            FILE_SAVE_TO_DIR_KEY, FILE_SAVE_TO_DIR_DEFAULT)
        self.set_save_to_dir.emit(self._save_to_dir)

        self._scihub_url = Preferences.get_or_default(
            NETWORK_SCIHUB_URL_KEY, NETWORK_SCIHUB_URL_DEFAULT)
        self._sess = get_session(self._scihub_url)
        self._scihub_api = None

    @property
    def window(self):
        return self._window

    def _connect(self):
        self._window.openSaveToDir.connect(self.open_save_to_dir)
        self._window.systemOpenSaveToDir.connect(self.system_open_save_to_dir)
        self._window.showUIPreference.connect(self.show_ui_preference)
        self._window.systemOpenLogFile.connect(self.system_open_log_file)
        self._window.systemOpenLogDirectory.connect(
            self.system_open_log_directory)
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
        self._ui_preferences.show.emit()
        center_window(self._ui_preferences.window, self._window)

    @Slot()
    def system_open_log_file(self):
        open_file(DEFAULT_LOG_FILE)

    @Slot()
    def system_open_log_directory(self):
        open_directory(DEFAULT_LOG_DIRECTORY)

    @Slot(str)
    def rampage(self, raw_query):
        scihub_url = Preferences.get_or_default(
            NETWORK_SCIHUB_URL_KEY, NETWORK_SCIHUB_URL_DEFAULT)
        if self._scihub_url != scihub_url:
            self._scihub_url = scihub_url
            self._sess = get_session(self._scihub_url)

        if os.path.exists(raw_query):
            if is_text_file(raw_query):
                self._query_list = deque()

                with open(raw_query, 'rt') as f:
                    for line in f:
                        cleaned_line = line.strip()
                        if cleaned_line != '':
                            self._query_list.append(cleaned_line)

                self._query_list_length = len(self._query_list)
                self.rampage_query_list()
            else:
                self._logger.error(LOGGER_SEP)
                self._logger.error(
                    self.tr('Query list file is not a text file!'))
        elif is_range_query(raw_query):
            self._query_list = deque(gen_range_query_list(raw_query))
            self._query_list_length = len(self._query_list)
            self.rampage_query_list()
        else:
            self.rampage_query(raw_query)

    def rampage_query_list(self):
        if self._query_list and len(self._query_list) > 0:
            self._logger.info(LOGGER_SEP)
            self._logger.info(self.tr('Dealing with {}/{} query ...').format(
                self._query_list_length - len(self._query_list) + 1,
                self._query_list_length))

            self.rampage_query(self._query_list.popleft())

    def rampage_query(self, query):
        del self._scihub_api
        gc.collect()

        self._scihub_api = SciHubAPI(
            self._logger,
            self.rampage_callback,
            self._scihub_url,
            self._sess,
            raw_query=query,
            query=query,
            rampage_type=SciHubAPIRampageType.RAW
        )

        self.before_rampage.emit()
        self._scihub_api.start()

    def rampage_with_typed_captcha(self, captcha_answer):
        self._scihub_api.captcha_answer = captcha_answer
        self.remove_captcha_img()
        self.before_rampage.emit()
        self._scihub_api.start()

    def rampage_callback(self, res, err):
        if err == SciHubAPIError.BLOCKED_BY_CAPTCHA:
            self.show_captcha(res)
        elif self._query_list:
            self.rampage_query_list()
        else:
            self.after_rampage.emit()

    def show_captcha(self, pdf_captcha_response):
        del self._scihub_api
        gc.collect()
        
        self._scihub_api = SciHubAPI(
            self._logger,
            self.rampage_callback,
            self._scihub_url,
            self._sess,
            raw_query=self._scihub_api.raw_query,
            query=pdf_captcha_response,
            rampage_type=SciHubAPIRampageType.WITH_CAPTCHA
        )

        _, captcha_img_url = self._scihub_api.get_captcha_info(pdf_captcha_response)
        captcha_img_file_path = self._scihub_api.download_captcha_img(captcha_img_url)
        self._captcha_img_file_path = captcha_img_file_path.resolve().as_posix()
        captcha_img_local_uri = captcha_img_file_path.as_uri()

        self._ui_captcha.show_ui_captcha.emit(captcha_img_local_uri)
        center_window(self._ui_captcha.window, self._window)

    def remove_captcha_img(self):
        if os.path.exists(self._captcha_img_file_path) and os.path.isfile(
                self._captcha_img_file_path):
            os.remove(self._captcha_img_file_path)
