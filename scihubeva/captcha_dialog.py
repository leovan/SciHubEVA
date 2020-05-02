#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from PySide2.QtCore import QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine


class CaptchaDialog(QObject):
    showWindowCaptcha = Signal(str)

    def __init__(self, parent, log=None):
        super(CaptchaDialog, self).__init__()

        self._parent = parent
        self.log = log

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/Captcha.qml')
        self._window = self._engine.rootObjects()[0]
        self._connect()

    def _connect(self):
        # Connect QML signals to PyQt slots
        self._window.killCaptcha.connect(self.killCaptcha)

        # Connect PyQt signals to QML slots
        self.showWindowCaptcha.connect(self._window.showWindowCaptcha)

    @Slot(bool, str)
    def killCaptcha(self, kill, captcha):
        if kill:
            self._parent.rampage_with_typed_captcha(captcha)
        else:
            self.log(self.tr('Battle canceled, rampage again?'), logging.ERROR)
            self._parent.afterRampage.emit()
