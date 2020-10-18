# -*- coding: utf-8 -*-

import re

from typing import List
from pdfminer.psparser import PSLiteral, PSKeyword


RANGE_QUERY_PATTERN = re.compile(r'\{\d+\-\d+\}')


def is_range_query(query_input: str) -> bool:
    if len(RANGE_QUERY_PATTERN.findall(query_input)) == 1:
        return True
    else:
        return False


def gen_range_query_list(query_input: str) -> List[str]:
    range_pattern = RANGE_QUERY_PATTERN.findall(query_input)[0]
    range_from_to = range_pattern.replace('{', '').replace('}', '').split('-')
    range_from = range_from_to[0]
    range_to = range_from_to[1]

    if len(range_from) == len(range_to):
        digit = len(range_from)
        range_item_pattern = '{:0>' + str(digit) + 'd}'
        range_items = [range_item_pattern.format(i) for i in range(int(range_from), int(range_to) + 1)]
    else:
        range_items = [str(i) for i in range(int(range_from), int(range_to) + 1)]

    return [query_input.replace(range_pattern, range_item) for range_item in range_items]


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


__all__ = [
    'RANGE_QUERY_PATTERN',
    'is_range_query',
    'gen_range_query_list',
    'make_pdf_metadata_str',
    'pdf_metadata_moddate_to_year'
]
