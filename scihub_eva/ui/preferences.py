# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtQml import QQmlApplicationEngine

from scihub_eva.globals.preferences import *
from scihub_eva.utils.sys_utils import *
from scihub_eva.utils.ui_utils import *
from scihub_eva.utils.preferences_utils import *
from scihub_eva.ui.add_scihub_url import UIAddSciHubURL


class UIPreferences(QObject):
    show = Signal()

    set_system_language = Signal(str)
    set_system_theme = Signal(str)

    set_file_filename_prefix_format = Signal(str)
    set_file_overwrite_existing_file = Signal(bool)

    set_network_scihub_urls = Signal(list)
    set_network_scihub_url = Signal(str)
    set_network_timeout = Signal(int)
    set_network_retry_times = Signal(int)
    set_network_proxy_enabled = Signal(bool)
    set_network_proxy_type = Signal(str)
    set_network_proxy_host = Signal(str)
    set_network_proxy_port = Signal(str)
    set_network_proxy_username = Signal(str)
    set_network_proxy_password = Signal(str)

    def __init__(self, parent):
        super(UIPreferences, self).__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/Preferences.qml')
        self._window = self._engine.rootObjects()[0]

        self._ui_add_scihub_url = UIAddSciHubURL(self)

        self._connect()
        self.load_preferences()

    def _connect(self):
        self._window.showUIAddSciHubURL.connect(self.show_ui_add_scihub_url)
        self._window.removeSciHubURL.connect(self.remove_scihub_url)

        self._window.saveSystemLanguage.connect(self.save_system_language)
        self._window.saveSystemTheme.connect(self.save_system_theme)
        self._window.saveFileFilenamePrefixFormat.connect(
            self.save_file_filename_prefix_format)
        self._window.saveFileOverwriteExistingFile.connect(
            self.save_file_overwrite_existing_file)
        self._window.saveNetworkSciHubURLs.connect(
            self.save_network_scihub_urls)
        self._window.saveNetworkSciHubURL.connect(self.save_network_scihub_url)
        self._window.saveNetworkTimeout.connect(self.save_network_timeout)
        self._window.saveNetworkRetryTimes.connect(
            self.save_network_retry_times)
        self._window.saveNetworkProxyEnabled.connect(
            self.save_network_proxy_enabled)
        self._window.saveNetworkProxyType.connect(self.save_network_proxy_type)
        self._window.saveNetworkProxyHost.connect(self.save_network_proxy_host)
        self._window.saveNetworkProxyPort.connect(self.save_network_proxy_port)
        self._window.saveNetworkProxyUsername.connect(
            self.save_network_proxy_username)
        self._window.saveNetworkProxyPassword.connect(
            self.save_network_proxy_password)

        self.show.connect(self._window.show)

        self.set_system_language.connect(self._window.setSystemLanguage)
        self.set_system_theme.connect(self._window.setSystemTheme)
        self.set_file_filename_prefix_format.connect(
            self._window.setFileFilenamePrefixFormat)
        self.set_file_overwrite_existing_file.connect(
            self._window.setFileOverwriteExistingFile)
        self.set_network_scihub_urls.connect(self._window.setNetworkSciHubURLs)
        self.set_network_scihub_url.connect(self._window.setNetworkSciHubURL)
        self.set_network_timeout.connect(self._window.setNetworkTimeout)
        self.set_network_retry_times.connect(self._window.setNetworkRetryTimes)
        self.set_network_proxy_enabled.connect(
            self._window.setNetworkProxyEnabled)
        self.set_network_proxy_type.connect(self._window.setNetworkProxyType)
        self.set_network_proxy_host.connect(self._window.setNetworkProxyHost)
        self.set_network_proxy_port.connect(self._window.setNetworkProxyPort)
        self.set_network_proxy_username.connect(
            self._window.setNetworkProxyUsername)
        self.set_network_proxy_password.connect(
            self._window.setNetworkProxyPassword)

    def load_preferences(self):
        self.set_system_language.emit(
            Preferences.get_or_default(SYSTEM_LANGUAGE_KEY, SYSTEM_LANGUAGE))
        self.set_system_theme.emit(
            QT_QUICK_CONTROLS2_CONFIG.get_or_default(
                'Material', 'Theme', SYSTEM_THEME_DEFAULT))
        self.set_file_filename_prefix_format.emit(
            Preferences.get_or_default(
                FILE_FILENAME_PREFIX_FORMAT_KEY,
                FILE_FILENAME_PREFIX_FORMAT_DEFAULT))
        self.set_file_overwrite_existing_file.emit(
            Preferences.get_or_default(
                FILE_OVERWRITE_EXISTING_FILE_KEY,
                FILE_OVERWRITE_EXISTING_FILE_DEFAULT, type=bool))

        self.set_network_scihub_urls.emit(
            Preferences.get_or_default(
                NETWORK_SCIHUB_URLS_KEY, NETWORK_SCIHUB_URLS_DEFAULT))
        self.set_network_scihub_url.emit(
            Preferences.get_or_default(
                NETWORK_SCIHUB_URL_KEY, NETWORK_SCIHUB_URL_DEFAULT))
        self.set_network_timeout.emit(
            Preferences.get_or_default(
                NETWORK_TIMEOUT_KEY, NETWORK_TIMEOUT_DEFAULT, type=int))
        self.set_network_retry_times.emit(
            Preferences.get_or_default(
                NETWORK_RETRY_TIMES_KEY, NETWORK_RETRY_TIMES_DEFAULT, type=int))
        self.set_network_proxy_enabled.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_ENABLE_KEY,
                NETWORK_PROXY_ENABLE_DEFAULT, type=bool))
        self.set_network_proxy_type.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_TYPE_KEY, NETWORK_PROXY_TYPE_DEFAULT))
        self.set_network_proxy_host.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_HOST_KEY, NETWORK_PROXY_HOST_DEFAULT))
        self.set_network_proxy_port.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_PORT_KEY, NETWORK_PROXY_PORT_DEFAULT))
        self.set_network_proxy_username.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_USERNAME_KEY, NETWORK_PROXY_USERNAME_DEFAULT))
        self.set_network_proxy_password.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_PASSWORD_KEY, NETWORK_PROXY_PASSWORD_DEFAULT))

    @property
    def window(self):
        return self._window

    @Slot()
    def show_ui_add_scihub_url(self):
        center_window(self._ui_add_scihub_url.window, self._window)
        self._ui_add_scihub_url.show.emit()

    @Slot(int)
    def remove_scihub_url(self, scihub_url_current_index):
        scihub_available_urls = Preferences.get_or_default(
            NETWORK_SCIHUB_URLS_KEY, NETWORK_SCIHUB_URLS_DEFAULT)
        del scihub_available_urls[scihub_url_current_index]

        Preferences.set(NETWORK_SCIHUB_URLS_KEY, scihub_available_urls)
        Preferences.set(NETWORK_SCIHUB_URL_KEY, scihub_available_urls[0])

        scihub_available_urls = Preferences.get_or_default(
            NETWORK_SCIHUB_URLS_KEY, NETWORK_SCIHUB_URLS_DEFAULT)
        self.set_network_scihub_urls.emit(scihub_available_urls)
        self.set_network_scihub_url.emit(scihub_available_urls[0])

    @Slot(str)
    def save_system_language(self, language):
        Preferences.set(SYSTEM_LANGUAGE_KEY, language)

    @Slot(str)
    def save_system_theme(self, theme):
        QT_QUICK_CONTROLS2_CONFIG.set('Material', 'Theme', theme)

    @Slot(str)
    def save_file_filename_prefix_format(self, filename_prefix_format):
        Preferences.set(FILE_FILENAME_PREFIX_FORMAT_KEY, filename_prefix_format)

    @Slot(bool)
    def save_file_overwrite_existing_file(self, overwrite):
        Preferences.set(FILE_OVERWRITE_EXISTING_FILE_KEY, overwrite)

    @Slot(list)
    def save_network_scihub_urls(self, scihub_urls):
        Preferences.set(NETWORK_SCIHUB_URLS_KEY, scihub_urls)

    @Slot(str)
    def save_network_scihub_url(self, scihub_url):
        Preferences.set(NETWORK_SCIHUB_URL_KEY, scihub_url)

    @Slot(int)
    def save_network_timeout(self, timeout):
        Preferences.set(NETWORK_TIMEOUT_KEY, timeout)

    @Slot(int)
    def save_network_retry_times(self, retry_times):
        Preferences.set(NETWORK_RETRY_TIMES_KEY, retry_times)

    @Slot(bool)
    def save_network_proxy_enabled(self, proxy_enabled):
        Preferences.set(NETWORK_PROXY_ENABLE_KEY, proxy_enabled)

    @Slot(str)
    def save_network_proxy_type(self, proxy_type):
        Preferences.set(NETWORK_PROXY_TYPE_KEY, proxy_type)

    @Slot(str)
    def save_network_proxy_host(self, proxy_host):
        Preferences.set(NETWORK_PROXY_HOST_KEY, proxy_host)

    @Slot(str)
    def save_network_proxy_port(self, proxy_port):
        Preferences.set(NETWORK_PROXY_PORT_KEY, proxy_port)

    @Slot(str)
    def save_network_proxy_username(self, proxy_username):
        Preferences.set(NETWORK_PROXY_USERNAME_KEY, proxy_username)

    @Slot(str)
    def save_network_proxy_password(self, proxy_password):
        Preferences.set(NETWORK_PROXY_PASSWORD_KEY, proxy_password)
