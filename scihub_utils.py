#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pdfminer.psparser import PSLiteral, PSKeyword

def make_pdf_metadata_str(value):
    if isinstance(value, bytes):
        metadata_str = value.decode('utf-8')
    elif isinstance(value, str):
        metadata_str = value
    elif isinstance(value, (PSLiteral, PSKeyword)):
        metadata_str = make_pdf_metadata_str(value.name)
    else:
        metadata_str = ''

    return metadata_str

def pdf_metadata_moddate_to_year(moddate: str):
    if moddate.startswith('D:'):
        year = moddate[2:6]
    else:
        year = moddate[:4]

    return year

if __name__ == '__main__':
    pass
