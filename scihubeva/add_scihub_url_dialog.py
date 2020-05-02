#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from PySide2.QtCore import QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine


class AddSciHubURLDialog(QObject):
    showWindowAddSciHubURL = Signal()

    def __init__(self, conf, parent):
        super(AddSciHubURLDialog, self).__init__()

        self._conf = conf
        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/AddSciHubURL.qml')
        self._window = self._engine.rootObjects()[0]
        self._connect()

    def _connect(self):
        # Connect QML signals to PyQt slots
        self._window.addSciHubURL.connect(self.addSciHubURL)

        # Connect PyQt signals to QML slots
        self.showWindowAddSciHubURL.connect(self._window.showWindowAddSciHubURL)

    @Slot(str)
    def addSciHubURL(self, url):
        scihub_available_urls = json.loads(self._conf.get('network', 'scihub_available_urls'))

        if url not in scihub_available_urls:
            scihub_available_urls.append(url)

        self._conf.set('network', 'scihub_available_urls', json.dumps(scihub_available_urls))
        self._parent.load_from_conf()
