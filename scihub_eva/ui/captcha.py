import logging
from typing import Any, cast

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QWindow
from PySide6.QtQml import QQmlApplicationEngine


class UICaptcha(QObject):
    show_ui_captcha = Signal(str)

    def __init__(self, parent: Any, logger: logging.Logger):
        super(UICaptcha, self).__init__()

        self._parent = parent
        self._logger = logger

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/Captcha.qml')
        self._window = self._engine.rootObjects()[0]
        self._connect()

    @property
    def window(self) -> QWindow:
        return cast(QWindow, self._window)

    def _connect(self) -> None:
        self.window.killCaptcha.connect(self.kill_captcha)

        self.show_ui_captcha.connect(self.window.showUICaptcha)

    @Slot(bool, str)
    def kill_captcha(self, kill: bool, captcha: str) -> None:
        if kill:
            self._parent.rampage_with_typed_captcha(captcha)
        else:
            self._logger.error(self.tr('Battle canceled, rampage again?'))
            self._parent.after_rampage.emit()
