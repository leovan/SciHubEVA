#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from PySide2.QtCore import QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine

from scihub_add_scihub_url import SciHubAddSciHubURL


class SciHubPreferences(QObject):
    showWindowPreferences = Signal()

    setFilenamePrefixFormat = Signal(str)
    setThemeModel = Signal(list)
    setThemeCurrentIndex = Signal(int)

    setNetworkSciHubURLModel = Signal(list)
    setNetworkSciHubURLCurrentIndex = Signal(int)
    setNetworkTimeout = Signal(int)
    setNetworkRetryTimes = Signal(int)

    setProxyEnabled = Signal(bool)
    setProxyType = Signal(str)
    setProxyHost = Signal(str)
    setProxyPort = Signal(int)
    setProxyUsername = Signal(str)
    setProxyPassword = Signal(str)

    def __init__(self, conf, qt_quick_controls2_conf):
        super(SciHubPreferences, self).__init__()

        self._conf = conf
        self._qt_quick_controls2_conf = qt_quick_controls2_conf
        self._themes = ['System', 'Light', 'Dark']

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/SciHubEVAPreferences.qml')
        self._window = self._engine.rootObjects()[0]
        self._connect()

        self.load_from_conf()

        self._scihub_add_scihub_url = SciHubAddSciHubURL(self._conf, self)

    def _connect(self):
        # Connect QML signals to PyQt slots
        self._window.showWindowAddSciHubURL.connect(self.showWindowAddSciHubURL)
        self._window.removeSciHubURL.connect(self.removeSciHubURL)

        self._window.saveFilenamePrefixFormat.connect(self.saveFilenamePrefixFormat)
        self._window.saveThemeCurrentIndex.connect(self.saveThemeCurrentIndex)

        self._window.saveNetworkSciHubURLCurrentIndex.connect(self.saveNetworkSciHubURLCurrentIndex)
        self._window.saveNetworkTimeout.connect(self.saveNetworkTimeout)
        self._window.saveNetworkRetryTimes.connect(self.saveNetworkRetryTimes)

        self._window.saveProxyEnabled.connect(self.saveProxyEnabled)
        self._window.saveProxyType.connect(self.saveProxyType)
        self._window.saveProxyHost.connect(self.saveProxyHost)
        self._window.saveProxyPort.connect(self.saveProxyPort)
        self._window.saveProxyUsername.connect(self.saveProxyUsername)
        self._window.saveProxyPassword.connect(self.saveProxyPassword)

        # Connect PyQt signals to QML slots
        self.showWindowPreferences.connect(self._window.showWindowPreferences)
        
        self.setFilenamePrefixFormat.connect(self._window.setFilenamePrefixFormat)
        self.setThemeModel.connect(self._window.setThemeModel)
        self.setThemeCurrentIndex.connect(self._window.setThemeCurrentIndex)

        self.setNetworkSciHubURLModel.connect(self._window.setNetworkSciHubURLModel)
        self.setNetworkSciHubURLCurrentIndex.connect(self._window.setNetworkSciHubURLCurrentIndex)
        self.setNetworkTimeout.connect(self._window.setNetworkTimeout)
        self.setNetworkRetryTimes.connect(self._window.setNetworkRetryTimes)

        self.setProxyEnabled.connect(self._window.setProxyEnabled)
        self.setProxyType.connect(self._window.setProxyType)
        self.setProxyHost.connect(self._window.setProxyHost)
        self.setProxyPort.connect(self._window.setProxyPort)
        self.setProxyUsername.connect(self._window.setProxyUsername)
        self.setProxyPassword.connect(self._window.setProxyPassword)

    def load_from_conf(self):
        self.setFilenamePrefixFormat.emit(self._conf.get('common', 'filename_prefix_format'))

        self.setThemeModel.emit(self._themes)
        theme = self._qt_quick_controls2_conf.get('Material', 'Theme')
        self.setThemeCurrentIndex.emit(self._themes.index(theme))

        scihub_available_urls = json.loads(self._conf.get('network', 'scihub_available_urls'))
        self.setNetworkSciHubURLModel.emit(scihub_available_urls)
        scihub_url = self._conf.get('network', 'scihub_url')
        self.setNetworkSciHubURLCurrentIndex.emit(scihub_available_urls.index(scihub_url))
        self.setNetworkTimeout.emit(self._conf.getint('network', 'timeout'))
        self.setNetworkRetryTimes.emit(self._conf.getint('network', 'retry_times'))

        self.setProxyEnabled.emit(self._conf.getboolean('proxy', 'enabled'))
        self.setProxyType.emit(self._conf.get('proxy', 'type'))
        self.setProxyHost.emit(self._conf.get('proxy', 'host'))
        self.setProxyPort.emit(self._conf.getint('proxy', 'port'))
        self.setProxyUsername.emit(self._conf.get('proxy', 'username'))
        self.setProxyPassword.emit(self._conf.get('proxy', 'password'))

    @Slot()
    def showWindowAddSciHubURL(self):
        self._scihub_add_scihub_url.showWindowAddSciHubURL.emit()

    @Slot(int)
    def removeSciHubURL(self, scihub_url_current_index):
        scihub_available_urls = json.loads(self._conf.get('network', 'scihub_available_urls'))
        del scihub_available_urls[scihub_url_current_index]

        self._conf.set('network', 'scihub_available_urls', json.dumps(scihub_available_urls))
        self._conf.set('network', 'scihub_url', scihub_available_urls[0])
        scihub_available_urls = json.loads(self._conf.get('network', 'scihub_available_urls'))
        self.setNetworkSciHubURLModel.emit(scihub_available_urls)
        self.setNetworkSciHubURLCurrentIndex.emit(0)

    @Slot(str)
    def saveFilenamePrefixFormat(self, filename_prefix_format):
        self._conf.set('common', 'filename_prefix_format', filename_prefix_format)

    @Slot(int)
    def saveThemeCurrentIndex(self, theme_current_index):
        self._qt_quick_controls2_conf.set('Material', 'Theme', self._themes[theme_current_index])

    @Slot(int)
    def saveNetworkSciHubURLCurrentIndex(self, scihub_url_current_index):
        scihub_available_urls = json.loads(self._conf.get('network', 'scihub_available_urls'))
        self._conf.set('network', 'scihub_url', scihub_available_urls[scihub_url_current_index])

    @Slot(int)
    def saveNetworkTimeout(self, timeout):
        self._conf.set('network', 'timeout', str(timeout))

    def saveNetworkRetryTimes(self, retry_times):
        self._conf.set('network', 'retry_times', str(retry_times))

    @Slot(bool)
    def saveProxyEnabled(self, enabled):
        self._conf.set('proxy', 'enabled', str(enabled).lower())

    @Slot(str)
    def saveProxyType(self, type):
        self._conf.set('proxy', 'type', type)

    @Slot(str)
    def saveProxyHost(self, host):
        self._conf.set('proxy', 'host', host)

    @Slot(int)
    def saveProxyPort(self, port):
        self._conf.set('proxy', 'port', str(port))

    @Slot(str)
    def saveProxyUsername(self, username):
        self._conf.set('proxy', 'username', username)

    @Slot(str)
    def saveProxyPassword(self, password):
        self._conf.set('proxy', 'password', password)
