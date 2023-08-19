#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sci-Hub EVA Version Updater

Usage:
    version_updater.py <version>
    version_updater.py (-h | --help)

Options:
    -h --help    Show this help
"""

import re
import os

from docopt import docopt


VERSION_PATTERN = r'\d+.\d+.\d+.\d+'

VERSION_FILES = [
    'macOS/Info.plist',
    'Windows/SciHubEVA.win.version',
    'Windows/SciHubEVA-x86_64.iss',
    '../scihub_eva/globals/versions.py'
]

VERSION_REPLACE_PATTERN = [
    r'<string>\d+.\d+.\d+</string>',
    r'filevers=\(\d+,\s*\d+,\s*\d+,\s*\d+\)',
    r'prodvers=\(\d+,\s*\d+,\s*\d+,\s*\d+\)',
    r"StringStruct\(u'FileVersion', u'\d+.\s*\d+.\s*\d+.\s*\d+'\)",
    r"StringStruct\(u'ProductVersion', u'\d+.\s*\d+.\s*\d+.\s*\d+'\)",
    r'#define MyAppVersion "\d+.\d+.\d+"',
    r"APPLICATION_VERSION = 'v\d+.\d+.\d+'"
]

VERSION_REPLACE_FORMATTER = [
    '<string>{major}.{minor}.{patch}</string>',
    'filevers=({major}, {minor}, {patch}, {build})',
    'prodvers=({major}, {minor}, {patch}, {build})',
    "StringStruct(u'FileVersion', u'{major}.{minor}.{patch}.{build}')",
    "StringStruct(u'ProductVersion', u'{major}.{minor}.{patch}.{build}')",
    '#define MyAppVersion "{major}.{minor}.{patch}"',
    "APPLICATION_VERSION = 'v{major}.{minor}.{patch}'"
]


def version_checker(version):
    if re.match(VERSION_PATTERN, version):
        version_ = version.split('.')
        version_dict = {
            'major': version_[0],
            'minor': version_[1],
            'patch': version_[2],
            'build': version_[3]
        }
        return version_dict, True
    else:
        return None, False


def replace_version(text, version):
    for replace_pattern, replace_formatter in \
            zip(VERSION_REPLACE_PATTERN, VERSION_REPLACE_FORMATTER):
        match_str = re.search(replace_pattern, text)
        replace_str = replace_formatter.format(**version)

        if match_str:
            return re.sub(replace_pattern, replace_str, text)

    return text


def update_version(version):
    for file in VERSION_FILES:
        backup_file = '{file}.bak'.format(file=file)
        os.rename(file, backup_file)

        with open(backup_file, 'r', encoding='utf-8') as fi, \
                open(file, 'w', encoding='utf-8') as fo:
            for line in fi:
                newline = replace_version(line, version)
                fo.write(newline)

                if newline != line:
                    print('{file}: \n{line} => \n{newline}'.format(
                        file=file, line=line, newline=newline))


if __name__ == '__main__':
    args = docopt(__doc__)

    if args['<version>']:
        version, valid = version_checker(args['<version>'])
        if valid:
            update_version(version)
        else:
            print('Please input version like X.X.X.X!')
