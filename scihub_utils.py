#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import subprocess

from pdfminer.psparser import PSLiteral, PSKeyword


def make_pdf_metadata_str(value) -> str:
    if isinstance(value, bytes):
        metadata_str = value.decode('utf-8')
    elif isinstance(value, str):
        metadata_str = value
    elif isinstance(value, (PSLiteral, PSKeyword)):
        metadata_str = make_pdf_metadata_str(value.name)
    else:
        metadata_str = ''

    return metadata_str


def pdf_metadata_moddate_to_year(moddate: str) -> str:
    if moddate.startswith('D:'):
        year = moddate[2:6]
    else:
        year = moddate[:4]

    return year


def show_directory(dir: str, timeout=1):
    if platform.system() == 'Darwin':
        subprocess.call(['open', dir], timeout=timeout)
    elif platform.system() == 'Windows':
        subprocess.call(['explorer', dir], timeout=timeout)
    else:
        subprocess.call(['xdg-open', dir], timeout=timeout)


def is_text_file(path: str) -> bool:
    try:
        with open(path, 'rt') as f:
            f.readlines()
    except:
        return False

    return True
