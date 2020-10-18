# -*- coding: utf-8 -*-


def center_window(window, parent_window):
    parent_window_center_x = parent_window.x() + int(parent_window.width() / 2)
    parent_window_center_y = parent_window.y() + int(parent_window.height() / 2)

    window_x = parent_window_center_x - int(window.width() / 2)
    window_y = parent_window_center_y - int(window.height() / 2)

    window.setPosition(window_x, window_y)


__all__ = [
    'center_window'
]
