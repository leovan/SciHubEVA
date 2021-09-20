# -*- coding: utf-8 -*-

import re
import tempfile
import threading
import time

from enum import Enum, unique
from urllib.parse import urlparse
from lxml import etree
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from tempfile import NamedTemporaryFile
from pathlib import Path
from PIL import Image, ImageOps

from PySide6.QtCore import QObject

from scihub_eva.globals.preferences import *
from scihub_eva.utils.preferences_utils import *
from scihub_eva.utils.network_utils import *
from scihub_eva.utils.logging_utils import *
from scihub_eva.utils.api_utils import *


@unique
class SciHubEVARampageType(Enum):
    # Original query
    ORIGINAL = 0

    # Query with typed captcha
    WITH_TYPED_CAPTCHA = 1


@unique
class SciHubAPIError(Enum):
    # Unknown error
    UNKNOWN = 0

    # Cannot find a valid iframe when fetching PDF URL
    NO_VALID_IFRAME = 1

    # Cannot download automatically due to captcha
    BLOCKED_BY_CAPTCHA = 2

    # Wrong captcha
    WRONG_CAPTCHA = 3


class SciHubAPI(QObject, threading.Thread):
    def __init__(self, query_input, query, logger, callback=None, rampage_type=None, **kwargs):
        QObject.__init__(self)
        threading.Thread.__init__(self)

        self._query_input = query_input
        self._query = query
        self._logger = logger
        self._callback = callback
        self._rampage_type = rampage_type

        if 'captcha_answer' in kwargs:
            self._captcha_answer = kwargs['captcha_answer']

        self._sess = get_session()
        self._doi_pattern = re.compile(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'])\S)+)\b')
        self._illegal_filename_pattern = re.compile(r'[\/\\\:\*\?\"\<\>\|]')

    def get_pdf_metadata(self, pdf):
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

            year = pdf_metadata_moddate_to_year(make_pdf_metadata_str(pdf_metadata.get('ModDate', '')))
            if year and year != '':
                metadata['year'] = year
        except Exception as e:
            pass

        temp_pdf_file.close()

        return metadata

    def guess_query_type(self, query):
        if query.startswith('http') or query.startswith('https'):
            if query.endswith('pdf'):
                query_type = 'pdf'
            else:
                query_type = 'url'
        elif query.isdigit():
            query_type = 'pmid'
        elif query.startswith('doi:') or self._doi_pattern.match(query):
            query_type = 'doi'
        else:
            query_type = 'string'

        return query_type

    def get_captcha_info(self, pdf_captcha_response):
        captcha_id, captcha_img_url = None, None

        html = etree.HTML(pdf_captcha_response.content)
        imgs = html.xpath('//img[@id="captcha"]')
        ids = html.xpath('//input[@name="id"]')

        if len(imgs) > 0 and len(ids) > 0:
            captcha_id = ids[0].attrib['value']
            captcha_img_src = imgs[0].attrib['src']

            if captcha_img_src.startswith('http'):
                captcha_img_url = captcha_img_src
            else:
                scheme, netloc, *_ = urlparse(pdf_captcha_response.url, scheme='http')
                captcha_img_url = scheme + '://' + netloc + captcha_img_src

        return captcha_id, captcha_img_url

    def download_captcha_img(self, captcha_img_url, invert_color=False):
        captcha_img_file = NamedTemporaryFile(delete=False)
        captcha_img_file_path = Path(captcha_img_file.name)

        captcha_img_res = self._sess.get(captcha_img_url, stream=True)

        if captcha_img_res.status_code == 200:
            for chuck in captcha_img_res:
                captcha_img_file.write(chuck)

        captcha_img_file.flush()
        captcha_img_file.close()

        if invert_color:
            img = Image.open(captcha_img_file_path).convert('RGB')
            invert_img = ImageOps.invert(img)
            img.close()
            invert_img.save(captcha_img_file_path, format='png')

        return captcha_img_file_path

    def fetch_pdf_with_captcha(self, pdf_captcha_response):
        pdf, err = None, None

        captcha_id, _ = self.get_captcha_info(pdf_captcha_response)

        pdf_response = self._sess.post(
            pdf_captcha_response.url, data={'answer': self._captcha_answer, 'id': captcha_id}, verify=False,
            timeout=Preferences.get_or_default(NETWORK_TIMEOUT_KEY, NETWORK_RETRY_TIMES_DEFAULT, type=int) / 1000.0)

        if pdf_response.headers['Content-Type'] == 'application/pdf':
            self._logger.info(self.tr('Angel [CAPTCHA] down!'))
            pdf = pdf_response.content
        else:
            pdf = pdf_response
            err = SciHubAPIError.WRONG_CAPTCHA

        return pdf, err

    def fetch_pdf(self, pdf_url):
        self._logger.info(self.tr('Fetching PDF ...'))

        pdf, err = None, None

        pdf_response = self._sess.get(
            pdf_url, verify=False,
            timeout=Preferences.get_or_default(NETWORK_TIMEOUT_KEY, NETWORK_RETRY_TIMES_DEFAULT, type=int) / 1000.0)

        if pdf_response.headers['Content-Type'] == 'application/pdf':
            pdf = pdf_response.content
        elif pdf_response.headers['Content-Type'].startswith('text/html'):
            self._logger.warn(self.tr('Angel [CAPTCHA] is coming!'))
            err = SciHubAPIError.BLOCKED_BY_CAPTCHA
            pdf = pdf_response
        else:
            self._logger.error(self.tr('Unknown PDF Content-Type!'))

        return pdf, err

    def fetch_pdf_url(self, query):
        scihub_url = Preferences.get_or_default(NETWORK_SCIHUB_URL_KEY, NETWORK_SCIHUB_URL_DEFAULT)
        self._logger.info(
            self.tr('Using Sci-Hub URL: ') + '<a href="{scihub_url}">{scihub_url}</a>'.format(scihub_url=scihub_url))

        query_type = self.guess_query_type(query)
        self._logger.info(self.tr('Query type: ') + query_type.upper())

        pdf_url = query
        err = None

        if query_type != 'pdf':
            try:
                self._logger.info(self.tr('Fetching PDF URL ...'))

                pdf_url_response = self._sess.post(
                    scihub_url, data={'request': query}, verify=False,
                    timeout=Preferences.get_or_default(
                        NETWORK_TIMEOUT_KEY, NETWORK_RETRY_TIMES_DEFAULT, type=int) / 1000.0)

                html = etree.HTML(pdf_url_response.content)
                article = html.xpath('//div[@id="article"]/embed[1]') if html is not None else None

                if article and len(article) > 0:
                    pdf_url = urlparse(article[0].attrib['src'], scheme='http').geturl()
                    pdf_url_html = '<a href="{pdf_url}">{pdf_url}</a>'.format(pdf_url=pdf_url)

                    self._logger.info(self.tr('Got PDF URL: ') + pdf_url_html)
                else:
                    err = SciHubAPIError.NO_VALID_IFRAME

                    self._logger.error(self.tr('Failed to get PDF URL!'))
                    self._logger.info(self.tr('You may need check it manually.'))
            except Exception as e:
                err = SciHubAPIError.UNKNOWN

                self._logger.error(self.tr('Failed to get PDF URL!'))
                self._logger.error(str(e))

        return pdf_url, err

    def save_pdf(self, pdf, filename):
        pdf_name_formatter = Preferences.get_or_default(
            FILE_FILENAME_PREFIX_FORMAT_KEY, FILE_FILENAME_PREFIX_FORMAT_DEFAULT)

        if not Preferences.get_or_default(
                FILE_OVERWRITE_EXISTING_FILE_KEY, FILE_OVERWRITE_EXISTING_FILE_DEFAULT, type=bool):
            pdf_name_formatter += '_' + str(round(time.time() * 1000000))

        pdf_metadata = self.get_pdf_metadata(pdf)
        query_type = self.guess_query_type(self._query_input)

        if query_type in ['doi', 'pmid']:
            pdf_metadata['id'] = self._query_input
        else:
            for patten in ['_{id}', '{id}_', '{id}']:
                pdf_name_formatter = pdf_name_formatter.replace(patten, '')

        pdf_name_formatter += '_' + filename if pdf_name_formatter else filename

        try:
            pdf_name = pdf_name_formatter.format(**pdf_metadata)
        except Exception as e:
            self._logger.error(self.tr('Unsupported filename keywords: ') + pdf_name_formatter)
            return

        pdf_name = self._illegal_filename_pattern.sub('-', pdf_name)
        pdf_path = str(Path(Preferences.get(FILE_SAVE_TO_DIR_KEY)) / pdf_name)

        with open(pdf_path, 'wb') as fp:
            fp.write(pdf)

        pdf_link = '<a href="file:///{pdf_path}">{pdf_path}</a>'.format(pdf_path=pdf_path)

        self._logger.info(self.tr('Saved PDF as: ') + pdf_link)

    def rampage(self, query, rampage_type):
        if rampage_type == SciHubEVARampageType.ORIGINAL:
            self._logger.info(LOGGER_SEP)
            self._logger.info(self.tr('Dealing with query: ') + query)

            # Fetch PDF URL
            pdf_url, err = self.fetch_pdf_url(query)
            if err is not None:
                return None, err

            # Fetch PDF
            pdf, err = self.fetch_pdf(pdf_url)
            if err == SciHubAPIError.BLOCKED_BY_CAPTCHA:
                return pdf, err
            elif err is not None:
                return None, err

            # Save PDF
            filename = urlparse(pdf_url).path[1:].split('/')[-1]
            self.save_pdf(pdf, filename)
        elif rampage_type == SciHubEVARampageType.WITH_TYPED_CAPTCHA:
            # Fetch PDF with Captcha
            pdf, err = self.fetch_pdf_with_captcha(query)
            if err == SciHubAPIError.WRONG_CAPTCHA:
                self._logger.error(self.tr('Wrong captcha, failed to kill Angel [CAPTCHA]!'))
                return None, err

            # Save PDF
            filename = urlparse(query.url).path[1:].split('/')[-1]
            self.save_pdf(pdf, filename)

        return None, None

    def run(self):
        res, err = self.rampage(self._query, self._rampage_type)
        self._callback(res, err)


__all__ = [
    'SciHubEVARampageType',
    'SciHubAPIError',
    'SciHubAPI'
]
