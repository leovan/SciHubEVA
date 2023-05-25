# -*- coding: utf-8 -*-

import re
import tempfile

from typing import List
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.psparser import PSLiteral, PSKeyword


RANGE_QUERY_PATTERN = re.compile(r'\{\d+\-\d+\}')
DOI_PATTERN = re.compile(
    r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'])\S)+)\b')


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
        range_items = [range_item_pattern.format(i) \
                       for i in range(int(range_from), int(range_to) + 1)]
    else:
        range_items = [
            str(i) for i in range(int(range_from), int(range_to) + 1)]

    return [query_input.replace(range_pattern, range_item) for range_item in
            range_items]


def guess_query_type(query):
    if query.startswith('http') or query.startswith('https'):
        if query.endswith('pdf'):
            query_type = 'pdf'
        else:
            query_type = 'url'
    elif query.isdigit():
        query_type = 'pmid'
    elif query.startswith('doi:') or DOI_PATTERN.match(query):
        query_type = 'doi'
    else:
        query_type = 'string'

    return query_type


def get_pdf_metadata(pdf) -> dict:
    temp_pdf_file = tempfile.TemporaryFile()
    temp_pdf_file.write(pdf)

    metadata = {
        'author': 'UNKNOWN_AUTHOR',
        'title': 'UNKNOWN_TITLE',
        'year': 'UNKNOWN_YEAR'
    }

    pdf_parser = PDFParser(temp_pdf_file)

    try:
        pdf_doc = PDFDocument(pdf_parser)
        pdf_metadata = pdf_doc.info[0]

        author = make_pdf_metadata_str(pdf_metadata.get('Author', ''))
        if author and author != '':
            metadata['author'] = author

        title = make_pdf_metadata_str(pdf_metadata.get('Title', ''))
        if title and title != '':
            metadata['title'] = title

        year = pdf_metadata_moddate_to_year(
            make_pdf_metadata_str(pdf_metadata.get('ModDate', '')))
        if year and year != '':
            metadata['year'] = year
    except Exception as e:
        pass

    temp_pdf_file.close()

    return metadata


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
    'guess_query_type',
    'get_pdf_metadata',
    'make_pdf_metadata_str',
    'pdf_metadata_moddate_to_year'
]
