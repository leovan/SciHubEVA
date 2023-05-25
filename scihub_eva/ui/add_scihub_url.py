# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtQml import QQmlApplicationEngine

from scihub_eva.globals.preferences import *
from scihub_eva.utils.preferences_utils import *


class UIAddSciHubURL(QObject):
    show = Signal()

    def __init__(self, parent):
        super(UIAddSciHubURL, self).__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/AddSciHubURL.qml')
        self._window = self._engine.rootObjects()[0]
        self._connect()

    @property
    def window(self):
        return self._window

    def _connect(self):
        self._window.addSciHubURL.connect(self.add_scihub_url)

        self.show.connect(self._window.showUIAddSciHubURL)

    @Slot(str)
    def add_scihub_url(self, url):
        scihub_available_urls = Preferences.get_or_default(
            NETWORK_SCIHUB_URLS_KEY, NETWORK_SCIHUB_URLS_DEFAULT)

        if url not in scihub_available_urls:
            scihub_available_urls.append(url)

        Preferences.set(NETWORK_SCIHUB_URLS_KEY, scihub_available_urls)
        self._parent.load_preferences()
