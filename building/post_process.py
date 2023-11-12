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
from pathlib import Path

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
    'QtBluetooth',
    'QtBodymovin',
    'QtCharts',
    'QtChartsQml',
    'QtDataVisualization',
    'QtDataVisualizationQml',
    'QtDesigner',
    'QtDesignerComponents',
    'QtLabsAnimation',
    'QtLanguageServer',
    'QtLabsWavefrontMesh',
    'QtLocation',
    'QtMultimedia',
    'QtMultimediaQuick',
    'QtMultimediaWidgets',
    'QtNetworkAuth',
    'QtNfc',
    'QtPdf',
    'QtPdfQuick',
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
    'QtSerialBus',
    'QtSerialPort',
    'QtShaderTools',
    'QtSpatialAudio',
    'QtSql',
    'QtStateMachine',
    'QtStateMachineQml',
    'QtTest',
    'QtTextToSpeech',
    'QtUiTools',
    'QtVirtualKeyboard',
    'QtWebChannel',
    'QtWebChannelQuick',
    'QtWebEngine',
    'QtWebEngineCore',
    'QtWebEngineQuick',
    'QtWebEngineQuickDelegatesQml',
    'QtWebSockets',
    'QtWebView',
    'QtWebViewQuick',
    'QtXmlPatterns',
]

USELESS_QT_DIRS = [
    'examples',
    'glue',
    'include',
    'scripts',
    'support',
    'translations',
    'typesystems',
    'Qt/lib/cmake',
    'Qt/lib/metatypes',
    'Qt/lib/objects-RelWithDebInfo',
    'Qt/libexec',
    'Qt/metatypes',
    'Qt/plugins/assetimporters',
    'Qt/plugins/canbus',
    'Qt/plugins/designer',
    'Qt/plugins/generic',
    'Qt/plugins/geometryloaders',
    'Qt/plugins/multimedia',
    'Qt/plugins/networkinformation',
    'Qt/plugins/platforminputcontexts',
    'Qt/plugins/position',
    'Qt/plugins/qmltooling',
    'Qt/plugins/renderers',
    'Qt/plugins/renderplugins',
    'Qt/plugins/sceneparsers',
    'Qt/plugins/scxmldatamodel',
    'Qt/plugins/sensors',
    'Qt/plugins/sqldrivers',
    'Qt/plugins/texttospeech',
    'Qt/plugins/tls',
    'Qt/plugins/virtualkeyboard',
    'Qt/translations',
]

USELESS_PACKAGES = [
    'PyInstaller',
    'tcl',
    'tcl8',
    'tk',
]

USELESS_LIBS = [
    'tcl',
    'tk',
]

DIST_INFO_DIRS_SUFFIX = [
    '.egg-info',
    '.dist-info'
]


def change_cwd():
    cwd = os.getcwd()

    if os.path.split(cwd)[1] == 'building':
        os.chdir(os.path.join(cwd, os.pardir))


def remove_files(files, path_func):
    for file in files:
        file_path = path_func(file)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)


def remove_pattern_files(files_pattern, path_func, recursive=False):
    for file_pattern in files_pattern:
        for file_path in glob.glob(path_func(file_pattern), recursive=recursive):
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)


def remove_dirs(dirs, path_func):
    for dir_ in dirs:
        dir_path = path_func(dir_)
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path, ignore_errors=True)


def remove_pattern_dirs(dirs_pattern, path_func, recursive=False):
    for dir_pattern in dirs_pattern:
        for dir_path in glob.glob(path_func(dir_pattern), recursive=recursive):
            if os.path.isdir(dir_path):
                shutil.rmtree(dir_path, ignore_errors=True)


def remove_dead_links(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                target = Path(file_path).resolve()
                if not os.path.exists(target):
                    os.remove(file_path)


def post_process_win(dist_folder):
    windows_app_path = os.path.join(dist_folder, 'SciHubEVA')

    path_func = lambda lib: os.path.join(windows_app_path, '_internal', 'PySide6', '{}.dll'.format(lib.replace('Qt', 'Qt6')))
    remove_files(USELESS_QT_LIBS, path_func)
    path_func = lambda lib: os.path.join(windows_app_path, '_internal', 'PySide6', 'qml', lib)
    remove_dirs(USELESS_QT_LIBS, path_func)

    path_func = lambda dir_prefix: os.path.join(windows_app_path, '_internal', 'PySide6', dir_prefix.replace('Qt/', ''))
    remove_dirs(USELESS_QT_DIRS, path_func)

    path_func = lambda package: os.path.join(windows_app_path, '_internal', package)
    remove_dirs(USELESS_PACKAGES, path_func)

    path_func = lambda library: os.path.join(windows_app_path, '_internal', 'lib{}*.dll'.format(library))
    remove_pattern_files(USELESS_LIBS, path_func)

    path_func = lambda dir_suffix:  os.path.join(windows_app_path, '_internal', '*{}'.format(dir_suffix))
    remove_pattern_dirs(DIST_INFO_DIRS_SUFFIX, path_func)


def post_process_macos(dist_folder):
    macos_app_path = os.path.join(dist_folder, 'Sci-Hub EVA.app')

    path_func = lambda lib: os.path.join(macos_app_path, 'Contents', 'Frameworks', 'PySide6', 'Qt', 'lib', '{}.framework'.format(lib))
    remove_dirs(USELESS_QT_LIBS, path_func)
    path_func = lambda lib: os.path.join(macos_app_path, 'Contents', 'Frameworks', 'PySide6', 'Qt', 'qml', lib)
    remove_dirs(USELESS_QT_LIBS, path_func)
    path_func = lambda lib: os.path.join(macos_app_path, 'Contents', 'Resources', 'PySide6', 'Qt', 'qml', lib)
    remove_dirs(USELESS_QT_LIBS, path_func)

    path_func = lambda dir_prefix: os.path.join(macos_app_path, 'Contents', 'Frameworks', 'PySide6', dir_prefix)
    remove_dirs(USELESS_QT_DIRS, path_func)
    path_func = lambda dir_prefix: os.path.join(macos_app_path, 'Contents', 'Resources', 'PySide6', dir_prefix)
    remove_dirs(USELESS_QT_DIRS, path_func)

    path_func = lambda package: os.path.join(macos_app_path, 'Contents', 'Frameworks', package)
    remove_dirs(USELESS_PACKAGES, path_func)
    path_func = lambda package: os.path.join(macos_app_path, 'Contents', 'Resources', package)
    remove_dirs(USELESS_PACKAGES, path_func)

    path_func = lambda library: os.path.join(macos_app_path, 'Contents', 'Frameworks', 'lib{}*.dylib'.format(library))
    remove_pattern_files(USELESS_LIBS, path_func)
    path_func = lambda library: os.path.join(macos_app_path, 'Contents', 'Resources', 'lib{}*.dylib'.format(library))
    remove_pattern_files(USELESS_LIBS, path_func)

    path_func = lambda dir_suffix:  os.path.join(macos_app_path, 'Contents', 'Frameworks', '*{}'.format(dir_suffix))
    remove_pattern_dirs(DIST_INFO_DIRS_SUFFIX, path_func)
    path_func = lambda dir_suffix:  os.path.join(macos_app_path, 'Contents', 'Resources', '*{}'.format(dir_suffix))
    remove_pattern_files(DIST_INFO_DIRS_SUFFIX, path_func)

    remove_dead_links(os.path.join(macos_app_path, 'Contents'))


def post_process_linux(dist_folder):
    linux_app_path = os.path.join(dist_folder, 'SciHubEVA')

    path_func = lambda lib: os.path.join(linux_app_path, '_internal', 'lib{}.so.6'.format(lib.replace('Qt', 'Qt6')))
    remove_files(USELESS_QT_LIBS, path_func)
    path_func = lambda lib: os.path.join(linux_app_path, '_internal', 'PySide6', 'Qt', 'qml', lib)
    remove_dirs(USELESS_QT_LIBS, path_func)

    path_func = lambda dir_prefix: os.path.join(linux_app_path, '_internal', 'PySide6', dir_prefix)
    remove_dirs(USELESS_QT_DIRS, path_func)

    path_func = lambda package: os.path.join(linux_app_path, '_internal', package)
    remove_dirs(USELESS_PACKAGES, path_func)

    path_func = lambda library: os.path.join(linux_app_path, '_internal', 'lib{}*.so*'.format(library))
    remove_pattern_files(USELESS_LIBS, path_func)

    path_func = lambda dir_suffix:  os.path.join(linux_app_path, '_internal', '*{}'.format(dir_suffix))
    remove_pattern_dirs(DIST_INFO_DIRS_SUFFIX, path_func)

    remove_dead_links(os.path.join(linux_app_path, '_internal'))


if __name__ == '__main__':
    args = docopt(__doc__)
    change_cwd()

    if is_windows():
        post_process_win(args['<dist-folder>'])
    elif is_macos():
        post_process_macos(args['<dist-folder>'])
    elif is_linux():
        post_process_linux(args['<dist-folder>'])
