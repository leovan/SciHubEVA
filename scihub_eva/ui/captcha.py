# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtQml import QQmlApplicationEngine


class UICaptcha(QObject):
    show_ui_captcha = Signal(str)

    def __init__(self, parent, logger):
        super(UICaptcha, self).__init__()

        self._parent = parent
        self._logger = logger

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/Captcha.qml')
        self._window = self._engine.rootObjects()[0]
        self._connect()

    @property
    def window(self):
        return self._window

    def _connect(self):
        self._window.killCaptcha.connect(self.kill_captcha)

        self.show_ui_captcha.connect(self._window.showUICaptcha)

    @Slot(bool, str)
    def kill_captcha(self, kill, captcha):
        if kill:
            self._parent.rampage_with_typed_captcha(captcha)
        else:
            self._logger.error(self.tr('Battle canceled, rampage again?'))
            self._parent.after_rampage.emit()
