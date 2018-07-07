#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.QtQml import QQmlApplicationEngine

from scihub_add_scihub_url import SciHubAddSciHubURL


class SciHubPreferences(QObject):
    showWindowPreferences = pyqtSignal()

    setFilenamePrefixFormat = pyqtSignal(str)

    setNetworkSciHubURLModel = pyqtSignal(list)
    setNetworkSciHubURLCurrentIndex = pyqtSignal(int)
    setNetworkTimeout = pyqtSignal(int)
    setNetworkRetryTimes = pyqtSignal(int)

    setProxyEnabled = pyqtSignal(bool)
    setProxyType = pyqtSignal(str)
    setProxyHost = pyqtSignal(str)
    setProxyPort = pyqtSignal(int)
    setProxyUsername = pyqtSignal(str)
    setProxyPassword = pyqtSignal(str)

    def __init__(self, conf):
        super(SciHubPreferences, self).__init__()

        self._conf = conf

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/SciHubEVAPreferences.qml')
        self._window = self._engine.rootObjects()[0]
        self._connect()

        self.loadFromConf()

        self._scihub_add_scihub_url = SciHubAddSciHubURL(self._conf, self)

    def _connect(self):
        # Connect QML signals to PyQt slots
        self._window.showWindowAddSciHubURL.connect(self.showWindowAddSciHubURL)
        self._window.removeSciHubURL.connect(self.removeSciHubURL)

        self._window.saveFilenamePrefixFormat.connect(self.saveFilenamePrefixFormat)

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

    def loadFromConf(self):
        self.setFilenamePrefixFormat.emit(self._conf.get('common', 'filename_prefix_format'))

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

    @pyqtSlot()
    def showWindowAddSciHubURL(self):
        self._scihub_add_scihub_url.showWindowAddSciHubURL.emit()

    @pyqtSlot(int)
    def removeSciHubURL(self, network__scihub_url_current_index):
        scihub_available_urls = json.loads(self._conf.get('network', 'scihub_available_urls'))
        del scihub_available_urls[network__scihub_url_current_index]

        self._conf.set('network', 'scihub_available_urls', json.dumps(scihub_available_urls))
        self._conf.set('network', 'scihub_url', scihub_available_urls[0])
        self.setNetworkSciHubURLCurrentIndex.emit(0)

    @pyqtSlot(str)
    def saveFilenamePrefixFormat(self, filename_prefix_format):
        self._conf.set('common', 'filename_prefix_format', filename_prefix_format)

    @pyqtSlot(int)
    def saveNetworkSciHubURLCurrentIndex(self, _scihub_url_current_index):
        scihub_available_urls = json.loads(self._conf.get('network', 'scihub_available_urls'))
        self._conf.set('network', 'scihub_url', scihub_available_urls[_scihub_url_current_index])

    @pyqtSlot(int)
    def saveNetworkTimeout(self, timeout):
        self._conf.set('network', 'timeout', str(timeout))

    def saveNetworkRetryTimes(self, retry_times):
        self._conf.set('network', 'retry_times', str(retry_times))

    @pyqtSlot(bool)
    def saveProxyEnabled(self, enabled):
        self._conf.set('proxy', 'enabled', str(enabled).lower())

    @pyqtSlot(str)
    def saveProxyType(self, type):
        self._conf.set('proxy', 'type', type)

    @pyqtSlot(str)
    def saveProxyHost(self, host):
        self._conf.set('proxy', 'host', host)

    @pyqtSlot(int)
    def saveProxyPort(self, port):
        self._conf.set('proxy', 'port', str(port))

    @pyqtSlot(str)
    def saveProxyUsername(self, username):
        self._conf.set('proxy', 'username', username)

    @pyqtSlot(str)
    def saveProxyPassword(self, password):
        self._conf.set('proxy', 'password', password)
