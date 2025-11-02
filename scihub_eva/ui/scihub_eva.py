import gc
import os
from collections import deque
from typing import Any, cast

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QWindow
from PySide6.QtQml import QQmlApplicationEngine

from scihub_eva.api.scihub_api import *
from scihub_eva.globals.preferences import *
from scihub_eva.globals.versions import *
from scihub_eva.ui.captcha import UICaptcha
from scihub_eva.ui.preferences import UIPreferences
from scihub_eva.utils.api_utils import *
from scihub_eva.utils.logging_utils import *
from scihub_eva.utils.network_utils import *
from scihub_eva.utils.preferences_utils import *
from scihub_eva.utils.sys_utils import *
from scihub_eva.utils.ui_utils import *


class UISciHubEVA(QObject):
    set_save_to_dir = Signal(str)
    append_log = Signal(str)
    before_rampage = Signal()
    after_rampage = Signal()

    def __init__(self) -> None:
        super(UISciHubEVA, self).__init__()

        self._engine = QQmlApplicationEngine()
        self._engine.rootContext().setContextProperty(
            'APPLICATION_VERSION', APPLICATION_VERSION
        )
        self._engine.rootContext().setContextProperty('PYTHON_VERSION', PYTHON_VERSION)
        self._engine.rootContext().setContextProperty('QT_VERSION', QT_VERSION)
        self._engine.load('qrc:/ui/SciHubEVA.qml')
        self._window = self._engine.rootObjects()[0]

        self._logger = DEFAULT_LOGGER
        self._logger.addHandler(UISciHubEVALogHandler(self))

        self._connect()

        self._ui_preferences = UIPreferences(self)
        self._ui_captcha = UICaptcha(self, self._logger)

        self._query_list = deque()
        self._query_list_length = 0
        self._captcha_img_file_path: str | None = None
        self._failed_queries = set()

        self._save_to_dir = Preferences.get_or_default(
            FILE_SAVE_TO_DIR_KEY, FILE_SAVE_TO_DIR_DEFAULT
        )
        self.set_save_to_dir.emit(self._save_to_dir)

        self._scihub_url = Preferences.get_or_default(
            API_SCIHUB_URL_KEY, API_SCIHUB_URL_DEFAULT
        )
        self._sess = get_session(self._scihub_url)
        self._scihub_api: SciHubAPI | None = None

    @property
    def window(self) -> QWindow:
        return cast(QWindow, self._window)

    def _connect(self) -> None:
        self.window.openSaveToDir.connect(self.open_save_to_dir)
        self.window.systemOpenSaveToDir.connect(self.system_open_save_to_dir)
        self.window.showUIPreference.connect(self.show_ui_preference)
        self.window.systemOpenLogFile.connect(self.system_open_log_file)
        self.window.systemOpenLogDirectory.connect(self.system_open_log_directory)
        self.window.exportFailedQueries.connect(self.export_failed_queries)
        self.window.rampage.connect(self.rampage)

        self.set_save_to_dir.connect(self.window.setSaveToDir)
        self.append_log.connect(self.window.appendLog)
        self.before_rampage.connect(self.window.beforeRampage)
        self.after_rampage.connect(self.window.afterRampage)

    @Slot(str)
    def open_save_to_dir(self, directory: str) -> None:
        self._save_to_dir = directory
        Preferences.set(FILE_SAVE_TO_DIR_KEY, directory)

    @Slot(str)
    def system_open_save_to_dir(self, directory: str) -> None:
        if os.path.exists(directory):
            open_directory(directory)

    @Slot()
    def show_ui_preference(self) -> None:
        self._ui_preferences.load_preferences()
        self._ui_preferences.show.emit()
        center_window(self._ui_preferences.window, self.window)

    @Slot()
    def system_open_log_file(self) -> None:
        open_file(DEFAULT_LOG_FILE)

    @Slot()
    def system_open_log_directory(self) -> None:
        open_directory(DEFAULT_LOG_DIRECTORY)

    @Slot(str)
    def export_failed_queries(self, path: str) -> None:
        with open(path, 'wt') as f:
            for failed_query in self._failed_queries:
                f.write(failed_query + '\n')

        self._failed_queries.clear()

    @Slot(str)
    def rampage(self, raw_query: str) -> None:
        scihub_url = Preferences.get_or_default(
            API_SCIHUB_URL_KEY, API_SCIHUB_URL_DEFAULT
        )
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
                self._logger.error(self.tr('Query list file is not a text file!'))
        elif is_range_query(raw_query):
            self._query_list = deque(gen_range_query_list(raw_query))
            self._query_list_length = len(self._query_list)
            self.rampage_query_list()
        else:
            self.rampage_query(raw_query)

    def rampage_query_list(self) -> None:
        if self._query_list and len(self._query_list) > 0:
            self._logger.info(LOGGER_SEP)
            self._logger.info(
                self.tr('Dealing with {}/{} query ...').format(
                    self._query_list_length - len(self._query_list) + 1,
                    self._query_list_length,
                )
            )

            self.rampage_query(self._query_list.popleft())

    def rampage_query(self, query: str) -> None:
        del self._scihub_api
        gc.collect()

        self._scihub_api = SciHubAPI(
            self._logger,
            self.rampage_callback,
            self._scihub_url,
            self._sess,
            raw_query=query,
            query=query,
            rampage_type=SciHubAPIRampageType.RAW,
        )

        self.before_rampage.emit()
        self._scihub_api.start()

    def rampage_with_typed_captcha(self, captcha_answer: str) -> None:
        self._scihub_api.captcha_answer = captcha_answer
        self.remove_captcha_img()
        self.before_rampage.emit()
        self._scihub_api.start()

    def rampage_callback(self, raw_query: str, res: Any, err: Any) -> None:
        if (
            err == SciHubAPIError.UNKNOWN
            or err == SciHubAPIError.WRONG_CAPTCHA
            or err == SciHubAPIError.NO_VALID_PDF
        ):
            self._failed_queries.add(raw_query)
        elif err is None:
            self._failed_queries.discard(raw_query)

        if err == SciHubAPIError.BLOCKED_BY_CAPTCHA:
            self.show_captcha(res)
        elif self._query_list:
            self.rampage_query_list()
        else:
            self.after_rampage.emit()

    def show_captcha(self, pdf_captcha_response: Any) -> None:
        raw_query = self._scihub_api.raw_query

        del self._scihub_api
        gc.collect()

        self._scihub_api = SciHubAPI(
            self._logger,
            self.rampage_callback,
            self._scihub_url,
            self._sess,
            raw_query=raw_query,
            query=pdf_captcha_response,
            rampage_type=SciHubAPIRampageType.WITH_CAPTCHA,
        )

        _, captcha_img_url = self._scihub_api.get_captcha_info(pdf_captcha_response)
        captcha_img_file_path = self._scihub_api.download_captcha_img(captcha_img_url)
        self._captcha_img_file_path = captcha_img_file_path.resolve().as_posix()
        captcha_img_local_uri = captcha_img_file_path.as_uri()

        self._ui_captcha.show_ui_captcha.emit(captcha_img_local_uri)
        center_window(self._ui_captcha.window, self.window)

    def remove_captcha_img(self) -> None:
        if os.path.exists(self._captcha_img_file_path) and os.path.isfile(
            self._captcha_img_file_path
        ):
            os.remove(self._captcha_img_file_path)
