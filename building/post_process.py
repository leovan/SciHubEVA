#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Post Process
Usage:
    post_process.py <dist-folder>
    post_process.py (-h | --help)
Options:
    -h --help    Show this help
"""

import os
import sys
import glob
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from docopt import docopt

from scihub_eva.utils.sys_utils import *


USELESS_QT_LIBS = [
    'Qt3D',
    'Qt3DAnimation',
    'Qt3DCore',
    'Qt3DExtras',
    'Qt3DInput',
    'Qt3DLogic',
    'Qt3DQuick',
    'Qt3DQuickAnimation',
    'Qt3DQuickExtras',
    'Qt3DQuickInput',
    'Qt3DQuickRender',
    'Qt3DQuickScene2D',
    'Qt3DRender',
    'Qt5Compat',
    'QtBodymovin',
    'QtCharts',
    'QtChartsQml',
    'QtDataVisualization',
    'QtDataVisualizationQml',
    'QtMultimedia',
    'QtMultimediaQuick',
    'QtLabsAnimation'
    'QtLabsWavefrontMesh'
    'QtPositioning',
    'QtPositioningQuick',
    'QtQuick3D',
    'QtQuick3DAssetImport',
    'QtQuick3DAssetUtils',
    'QtQuick3DEffects',
    'QtQuick3DHelpers',
    'QtQuick3DParticleEffects',
    'QtQuick3DParticles',
    'QtQuick3DRuntimeRender',
    'QtQuick3DUtils',
    'QtQuickTest',
    'QtQuickTimeline',
    'QtRemoteObjects',
    'QtRemoteObjectsQml',
    'QtScxml',
    'QtScxmlQml',
    'QtSensors',
    'QtSensorsQuick',
    'QtShaderTools',
    'QtSql',
    'QtStateMachine',
    'QtStateMachineQml',
    'QtTest',
    'QtVirtualKeyboard',
    'QtWebChannel',
    'QtWebEngine',
    'QtWebEngineCore',
    'QtWebEngineQuick',
    'QtWebEngineQuickDelegatesQml',
    'QtWebSockets',
    'QtWebView',
    'QtWebViewQuick',
    'QtXmlPatterns'
]


USELESS_PACKAGES = [
    'PyInstaller',
    'tcl',
    'tcl8',
    'tk'
]

USELESS_LIBRARIES = [
    'tcl',
    'tk'
]


def change_cwd():
    cwd = os.getcwd()

    if os.path.split(cwd)[1] == 'building':
        os.chdir(os.path.join(cwd, os.pardir))


def post_process_win(dist_folder):
    windows_app_path = os.path.join(dist_folder, 'SciHubEVA')

    # remove useless Qt modules
    for qt_lib in USELESS_QT_LIBS:
        qt_lib_win = qt_lib.replace('Qt', 'Qt6')
        qt_lib_win += '.dll'
        qt_lib_path = os.path.join(windows_app_path, 'PySide6', qt_lib_win)
        if os.path.exists(qt_lib_path):
            os.remove(qt_lib_path)

        qt_qml_dir = os.path.join(windows_app_path, 'PySide6', 'qml', qt_lib)
        if os.path.isdir(qt_qml_dir):
            shutil.rmtree(qt_qml_dir, ignore_errors=True)

    # remove useless packages
    for package in USELESS_PACKAGES:
        package_dir = os.path.join(windows_app_path, package)

        if os.path.isdir(package_dir):
            shutil.rmtree(package_dir, ignore_errors=True)

    # remove useless libraries
    for library in USELESS_LIBRARIES:
        for lib in glob.glob(
                os.path.join(windows_app_path, 'lib{}*.dll'.format(library)), recursive=False):
            os.remove(lib)

    # remove useless directory
    for postfix in ['.egg-info', '.dist-info']:
        for directory in glob.glob(
                os.path.join(windows_app_path, '*{}'.format(postfix)), recursive=False):
            if os.path.isdir(directory):
                shutil.rmtree(directory, ignore_errors=True)


def post_process_macos(dist_folder):
    macos_app_path = os.path.join(dist_folder, 'SciHubEVA.app')

    # remove useless Qt modules
    for qt_lib in USELESS_QT_LIBS:
        qt_lib_path = os.path.join(macos_app_path, 'Contents', 'MacOS', qt_lib)
        if os.path.exists(qt_lib_path):
            os.remove(qt_lib_path)

        qt_qml_dir = os.path.join(macos_app_path, 'Contents', 'MacOS', 'PySide6', 'Qt', 'qml', qt_lib)
        if os.path.isdir(qt_qml_dir):
            shutil.rmtree(qt_qml_dir, ignore_errors=True)

    # remove useless packages
    for package in USELESS_PACKAGES:
        package_dir = os.path.join(macos_app_path, 'Contents', 'Resources', package)
        package_link = os.path.join(macos_app_path, 'Contents', 'MacOS', package)

        if os.path.isdir(package_dir):
            shutil.rmtree(package_dir, ignore_errors=True)

        if os.path.islink(package_link):
            os.remove(package_link)

    # remove useless libraries
    for library in USELESS_LIBRARIES:
        for lib in glob.glob(
                os.path.join(macos_app_path, 'Contents', 'MacOS', 'lib{}*.dylib'.format(library)), recursive=False):
            os.remove(lib)

    # remove useless directory
    for postfix in ['.egg-info', '.dist-info']:
        for directory in glob.glob(
                os.path.join(macos_app_path, 'Contents', 'Resources', '*{}'.format(postfix)), recursive=False):
            if os.path.isdir(directory):
                shutil.rmtree(directory, ignore_errors=True)

        for directory in glob.glob(
                os.path.join(macos_app_path, 'Contents', 'MacOS', '*{}'.format(postfix)), recursive=False):
            if os.path.islink(directory):
                os.remove(directory)


if __name__ == '__main__':
    args = docopt(__doc__)
    change_cwd()

    if is_windows():
        post_process_win(args['<dist-folder>'])
    elif is_macos():
        post_process_macos(args['<dist-folder>'])
