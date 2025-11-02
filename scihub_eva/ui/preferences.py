from typing import Any, cast

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QWindow
from PySide6.QtQml import QQmlApplicationEngine

from scihub_eva.globals.preferences import *
from scihub_eva.ui.add_scihub_url import UIAddSciHubURL
from scihub_eva.utils.preferences_utils import *
from scihub_eva.utils.sys_utils import *
from scihub_eva.utils.ui_utils import *


class UIPreferences(QObject):
    show = Signal()

    set_appearance_language = Signal(str)
    set_appearance_theme = Signal(str)

    set_file_filename_prefix_format = Signal(str)
    set_file_overwrite_existing_file = Signal(bool)

    set_api_scihub_urls = Signal(list)
    set_api_scihub_url = Signal(str)
    set_api_pdf_xpaths = Signal(str)
    set_api_captcha_id_xpaths = Signal(str)
    set_api_captcha_image_xpaths = Signal(str)
    set_network_timeout = Signal(int)
    set_network_retry_times = Signal(int)
    set_network_proxy_enabled = Signal(bool)
    set_network_proxy_type = Signal(str)
    set_network_proxy_host = Signal(str)
    set_network_proxy_port = Signal(str)
    set_network_proxy_username = Signal(str)
    set_network_proxy_password = Signal(str)

    def __init__(self, parent: Any) -> None:
        super(UIPreferences, self).__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/Preferences.qml')
        self._window = self._engine.rootObjects()[0]

        self._ui_add_scihub_url = UIAddSciHubURL(self)

        self._connect()
        self.load_preferences()

    @property
    def window(self) -> QWindow:
        return cast(QWindow, self._window)

    def _connect(self) -> None:
        self.window.showUIAddSciHubURL.connect(self.show_ui_add_scihub_url)
        self.window.removeSciHubURL.connect(self.remove_scihub_url)

        self.window.saveApiSciHubURLs.connect(self.save_api_scihub_urls)
        self.window.saveApiSciHubURL.connect(self.save_api_scihub_url)
        self.window.saveApiPDFXPaths.connect(self.save_api_pdf_xpaths)
        self.window.saveApiCaptchaIdXPaths.connect(self.save_api_captcha_id_xpaths)
        self.window.saveApiCaptchaImageXPaths.connect(
            self.save_api_captcha_image_xpaths
        )

        self.window.saveAppearanceLanguage.connect(self.save_appearance_language)
        self.window.saveAppearanceTheme.connect(self.save_appearance_theme)

        self.window.saveFileFilenamePrefixFormat.connect(
            self.save_file_filename_prefix_format
        )
        self.window.saveFileOverwriteExistingFile.connect(
            self.save_file_overwrite_existing_file
        )

        self.window.saveNetworkTimeout.connect(self.save_network_timeout)
        self.window.saveNetworkRetryTimes.connect(self.save_network_retry_times)
        self.window.saveNetworkProxyEnabled.connect(self.save_network_proxy_enabled)
        self.window.saveNetworkProxyType.connect(self.save_network_proxy_type)
        self.window.saveNetworkProxyHost.connect(self.save_network_proxy_host)
        self.window.saveNetworkProxyPort.connect(self.save_network_proxy_port)
        self.window.saveNetworkProxyUsername.connect(self.save_network_proxy_username)
        self.window.saveNetworkProxyPassword.connect(self.save_network_proxy_password)

        self.show.connect(self.window.show)

        self.set_api_scihub_urls.connect(self.window.setApiSciHubURLs)
        self.set_api_scihub_url.connect(self.window.setApiSciHubURL)
        self.set_api_pdf_xpaths.connect(self.window.setApiPDFXPaths)
        self.set_api_captcha_id_xpaths.connect(self.window.setApiCaptchaIdXPaths)
        self.set_api_captcha_image_xpaths.connect(self.window.setApiCaptchaImageXPaths)

        self.set_appearance_language.connect(self.window.setAppearanceLanguage)
        self.set_appearance_theme.connect(self.window.setAppearanceTheme)

        self.set_file_filename_prefix_format.connect(
            self.window.setFileFilenamePrefixFormat
        )
        self.set_file_overwrite_existing_file.connect(
            self.window.setFileOverwriteExistingFile
        )

        self.set_network_timeout.connect(self.window.setNetworkTimeout)
        self.set_network_retry_times.connect(self.window.setNetworkRetryTimes)
        self.set_network_proxy_enabled.connect(self.window.setNetworkProxyEnabled)
        self.set_network_proxy_type.connect(self.window.setNetworkProxyType)
        self.set_network_proxy_host.connect(self.window.setNetworkProxyHost)
        self.set_network_proxy_port.connect(self.window.setNetworkProxyPort)
        self.set_network_proxy_username.connect(self.window.setNetworkProxyUsername)
        self.set_network_proxy_password.connect(self.window.setNetworkProxyPassword)

    def load_preferences(self) -> None:
        self.set_appearance_language.emit(
            Preferences.get_or_default(APPEARANCE_LANGUAGE_KEY, SYSTEM_LANGUAGE)
        )
        self.set_appearance_theme.emit(
            Preferences.get_or_default(APPEARANCE_THEME_KEY, APPEARANCE_THEME_DEFAULT)
        )

        self.set_api_scihub_urls.emit(
            Preferences.get_or_default(API_SCIHUB_URLS_KEY, API_SCIHUB_URLS_DEFAULT)
        )
        self.set_api_scihub_url.emit(
            Preferences.get_or_default(API_SCIHUB_URL_KEY, API_SCIHUB_URL_DEFAULT)
        )

        pdf_xpath_list = Preferences.get_or_default(
            API_PDF_XPATHS_KEY, API_PDF_XPATHS_DEFAULT
        )
        pdf_xpaths = '\n'.join(pdf_xpath_list)
        self.set_api_pdf_xpaths.emit(pdf_xpaths)

        captcha_id_xpath_list = Preferences.get_or_default(
            API_CAPTCHA_ID_XPATHS_KEY, API_CAPTCHA_ID_XPATHS_DEFAULT
        )
        captcha_id_xpaths = '\n'.join(captcha_id_xpath_list)
        self.set_api_captcha_id_xpaths.emit(captcha_id_xpaths)

        captcha_image_xpath_list = Preferences.get_or_default(
            API_CAPTCHA_IMAGE_XPATHS_KEY, API_CAPTCHA_IMAGE_XPATHS_DEFAULT
        )
        captcha_image_xpaths = '\n'.join(captcha_image_xpath_list)
        self.set_api_captcha_image_xpaths.emit(captcha_image_xpaths)

        self.set_file_filename_prefix_format.emit(
            Preferences.get_or_default(
                FILE_FILENAME_PREFIX_FORMAT_KEY, FILE_FILENAME_PREFIX_FORMAT_DEFAULT
            )
        )
        self.set_file_overwrite_existing_file.emit(
            Preferences.get_or_default(
                FILE_OVERWRITE_EXISTING_FILE_KEY,
                FILE_OVERWRITE_EXISTING_FILE_DEFAULT,
                value_type=bool,
            )
        )

        self.set_network_timeout.emit(
            Preferences.get_or_default(
                NETWORK_TIMEOUT_KEY, NETWORK_TIMEOUT_DEFAULT, value_type=int
            )
        )
        self.set_network_retry_times.emit(
            Preferences.get_or_default(
                NETWORK_RETRY_TIMES_KEY, NETWORK_RETRY_TIMES_DEFAULT, value_type=int
            )
        )
        self.set_network_proxy_enabled.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_ENABLE_KEY, NETWORK_PROXY_ENABLE_DEFAULT, value_type=bool
            )
        )
        self.set_network_proxy_type.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_TYPE_KEY, NETWORK_PROXY_TYPE_DEFAULT
            )
        )
        self.set_network_proxy_host.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_HOST_KEY, NETWORK_PROXY_HOST_DEFAULT
            )
        )
        self.set_network_proxy_port.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_PORT_KEY, NETWORK_PROXY_PORT_DEFAULT
            )
        )
        self.set_network_proxy_username.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_USERNAME_KEY, NETWORK_PROXY_USERNAME_DEFAULT
            )
        )
        self.set_network_proxy_password.emit(
            Preferences.get_or_default(
                NETWORK_PROXY_PASSWORD_KEY, NETWORK_PROXY_PASSWORD_DEFAULT
            )
        )

    @Slot()
    def show_ui_add_scihub_url(self) -> None:
        center_window(self._ui_add_scihub_url.window, self.window)
        self._ui_add_scihub_url.show.emit()

    @Slot(int)
    def remove_scihub_url(self, scihub_url_current_index: int) -> None:
        scihub_available_urls = Preferences.get_or_default(
            API_SCIHUB_URLS_KEY, API_SCIHUB_URLS_DEFAULT
        )
        del scihub_available_urls[scihub_url_current_index]

        Preferences.set(API_SCIHUB_URLS_KEY, scihub_available_urls)
        Preferences.set(API_SCIHUB_URL_KEY, scihub_available_urls[0])

        scihub_available_urls = Preferences.get_or_default(
            API_SCIHUB_URLS_KEY, API_SCIHUB_URLS_DEFAULT
        )
        self.set_api_scihub_urls.emit(scihub_available_urls)
        self.set_api_scihub_url.emit(scihub_available_urls[0])

    @Slot(list)
    def save_api_scihub_urls(self, scihub_urls: list[str]) -> None:
        Preferences.set(API_SCIHUB_URLS_KEY, scihub_urls)

    @Slot(str)
    def save_api_scihub_url(self, scihub_url: str) -> None:
        Preferences.set(API_SCIHUB_URL_KEY, scihub_url)

    @Slot(str)
    def save_api_pdf_xpaths(self, pdf_xpaths: str) -> None:
        pdf_xpath_list = [
            pdf_xpath.strip()
            for pdf_xpath in pdf_xpaths.split('\n')
            if pdf_xpath.strip() != ''
        ]

        Preferences.set(API_PDF_XPATHS_KEY, pdf_xpath_list)

    @Slot(str)
    def save_api_captcha_id_xpaths(self, captcha_id_xpaths: str) -> None:
        captcha_id_xpath_list = [
            captcha_id_xpath.strip()
            for captcha_id_xpath in captcha_id_xpaths.split('\n')
            if captcha_id_xpath.strip() != ''
        ]

        Preferences.set(API_CAPTCHA_ID_XPATHS_KEY, captcha_id_xpath_list)

    @Slot(str)
    def save_api_captcha_image_xpaths(self, captcha_image_xpaths: str) -> None:
        captcha_image_xpath_list = [
            captcha_image_xpath.strip()
            for captcha_image_xpath in captcha_image_xpaths.split('\n')
            if captcha_image_xpath.strip() != ''
        ]

        Preferences.set(API_CAPTCHA_IMAGE_XPATHS_KEY, captcha_image_xpath_list)

    @Slot(str)
    def save_appearance_language(self, language: str) -> None:
        Preferences.set(APPEARANCE_LANGUAGE_KEY, language)

    @Slot(str)
    def save_appearance_theme(self, theme: str) -> None:
        Preferences.set(APPEARANCE_THEME_KEY, theme)

    @Slot(str)
    def save_file_filename_prefix_format(self, filename_prefix_format: str) -> None:
        Preferences.set(FILE_FILENAME_PREFIX_FORMAT_KEY, filename_prefix_format)

    @Slot(bool)
    def save_file_overwrite_existing_file(self, overwrite: bool) -> None:
        Preferences.set(FILE_OVERWRITE_EXISTING_FILE_KEY, overwrite)

    @Slot(int)
    def save_network_timeout(self, timeout: int) -> None:
        Preferences.set(NETWORK_TIMEOUT_KEY, timeout)

    @Slot(int)
    def save_network_retry_times(self, retry_times: int) -> None:
        Preferences.set(NETWORK_RETRY_TIMES_KEY, retry_times)

    @Slot(bool)
    def save_network_proxy_enabled(self, proxy_enabled: bool) -> None:
        Preferences.set(NETWORK_PROXY_ENABLE_KEY, proxy_enabled)

    @Slot(str)
    def save_network_proxy_type(self, proxy_type: str) -> None:
        Preferences.set(NETWORK_PROXY_TYPE_KEY, proxy_type)

    @Slot(str)
    def save_network_proxy_host(self, proxy_host: str) -> None:
        Preferences.set(NETWORK_PROXY_HOST_KEY, proxy_host)

    @Slot(str)
    def save_network_proxy_port(self, proxy_port: str) -> None:
        Preferences.set(NETWORK_PROXY_PORT_KEY, proxy_port)

    @Slot(str)
    def save_network_proxy_username(self, proxy_username: str) -> None:
        Preferences.set(NETWORK_PROXY_USERNAME_KEY, proxy_username)

    @Slot(str)
    def save_network_proxy_password(self, proxy_password: str) -> None:
        Preferences.set(NETWORK_PROXY_PASSWORD_KEY, proxy_password)
