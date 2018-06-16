#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
import tempfile
import threading

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from urllib.parse import urlparse
from lxml import etree

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

from PyQt5.QtCore import QObject

from scihub_conf import SciHubConf
from scihub_utils import make_pdf_metadata_str, pdf_metadata_moddate_to_year

class SciHubAPI(QObject, threading.Thread):
    def __init__(self, query, callback=None, conf=None, log=None):
        QObject.__init__(self)
        threading.Thread.__init__(self)

        self._query = query
        self._callback = callback

        if conf:
            self._conf = conf
        else:
            self._conf = SciHubConf()

        if log:
            self.log = log

        self._sess = requests.Session()
        self._sess.headers = json.loads(self._conf.get('network', 'session_header'))

        retry_times = self._conf.getint('network', 'retry_times')
        retry = Retry(total=retry_times, read=retry_times, connect=retry_times)
        adapter = HTTPAdapter(max_retries=retry)
        self._sess.mount('http://', adapter)
        self._sess.mount('https://', adapter)

        self._set_http_proxy()

        self._doi_pattern = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'])\S)+)\b'
        self._illegal_filename_pattern = r'[\/\\\:\*\?\"\<\>\|]'

    def log(self, message, type=None):
        if type:
            log_formater = '[{type}] - {message}'
        else:
            log_formater = '{message}'

        print(log_formater.format(type=type, message=message))

    def _set_http_proxy(self):
        if self._conf.getboolean('proxy', 'enabled'):
            proxy_type = self._conf.get('proxy', 'type')
            proxy_host = self._conf.get('proxy', 'host')
            proxy_port = self._conf.get('proxy', 'port')
            proxy_username = self._conf.get('proxy', 'username')
            proxy_password = self._conf.get('proxy', 'password')

            proxy = proxy_type + '://'

            if proxy_username and proxy_username != '':
                proxy += proxy_username

            if proxy_password and proxy_password != '':
                proxy += proxy_password

            if proxy_username and proxy_username != '':
                proxy += '@'

            proxy += proxy_host

            if proxy_port and proxy_port!= '':
                proxy += ':' + proxy_port

            self._sess.proxies = {'http': proxy, 'https': proxy}

    def get_pdf_metadata(self, pdf_file_stream):
        metadata = {'author': 'UNKNOWN_AUTHOR',
                    'title': 'UNKNOWN_TITLE',
                    'year': 'UNKNOWN_YEAR'}

        pdf_parser = PDFParser(pdf_file_stream)
        pdf_doc = PDFDocument(pdf_parser)
        pdf_metadata = pdf_doc.info[0]

        author = make_pdf_metadata_str(pdf_metadata['Author'] if 'Author' in pdf_metadata else '')
        if author and author != '':
            metadata['author'] = author

        title = make_pdf_metadata_str(pdf_metadata['Title'] if 'Title' in pdf_metadata else '')
        if title and title != '':
            metadata['title'] = title

        year = pdf_metadata_moddate_to_year(
            make_pdf_metadata_str(pdf_metadata['ModDate'] if 'ModDate' in pdf_metadata else ''))
        if year and year != '':
            metadata['year'] = year

        return metadata

    def guess_query_type(self, query):
        if query.startswith('http') or query.startswith('https'):
            if query.endswith('pdf'):
                query_type = 'pdf'
            else:
                query_type = 'url'
        elif query.isdigit():
            query_type = 'pmid'
        elif query.startswith('doi:') or re.match(self._doi_pattern, query):
            query_type = 'doi'
        else:
            query_type = 'string'

        log_formater = self.tr('Query type: ') + '{query_type}'
        self.log(log_formater.format(query_type=query_type.upper()), 'INFO')

        return query_type

    def fetch(self, query):
        query_type = self.guess_query_type(query)
        data = {}

        current_scihub_url = self._conf.get('network', 'scihub_url')
        scihub_available_urls = json.loads(self._conf.get('network', 'scihub_available_urls'))
        current_scihub_url_index = scihub_available_urls.index(current_scihub_url)

        scihub_available_urls_ = scihub_available_urls[current_scihub_url_index:]
        scihub_available_urls_.extend(scihub_available_urls[:current_scihub_url_index])

        for round, scihub_url in enumerate(scihub_available_urls_):
            data = {}

            log_formater = self.tr('Using Sci-Hub URL: ') + '{scihub_url}'
            self.log(log_formater.format(scihub_url=scihub_url), 'INFO')
            self._conf.set('network', 'scihub_url', scihub_url)

            pdf_url = query

            if query_type != 'pdf':
                pdf_query_url = 'http://{scihub_url}'.format(scihub_url=scihub_url)

                try:
                    self.log(self.tr('Fetching PDF URL ...'), 'INFO')

                    pdf_url_response = self._sess.post(
                        pdf_query_url, data={'request': query}, verify=False,
                        timeout=self._conf.getfloat('network', 'timeout') / 1000.0)

                    html = etree.HTML(pdf_url_response.content)
                    iframes = html.xpath('//iframe')

                    if len(iframes) > 0:
                        iframe = iframes[0]
                        pdf_url = iframe.attrib['src']

                        log_formater = self.tr('Got PDF URL: ') + '{pdf_url}'
                        self.log(log_formater.format(pdf_url=pdf_url), 'INFO')
                    else:
                        data['error'] = self.tr('No valide iframe!')
                        self.log(self.tr('Failed to get PDF URL!'), 'ERROR')
                        self.log(data['error'], 'ERROR')
                except Exception as err:
                    data['error'] = str(err)
                    self.log(self.tr('Failed to get PDF!'), 'ERROR')
                    self.log(data['error'], 'ERROR')

            if not 'error' in data:
                filename = urlparse(pdf_url).path[1:].split('/')[-1]
                data['filename'] = re.sub(self._illegal_filename_pattern, '_', filename)

                self.log(self.tr('Fetching PDF ...'), 'INFO')

                try:
                    pdf_response = self._sess.get(
                        pdf_url, verify=False,
                        timeout=self._conf.getfloat('network', 'timeout') / 1000.0)

                    if pdf_response.headers['Content-Type'] == 'application/pdf':
                        data['pdf'] = pdf_response.content

                        temp_pdf_file = tempfile.TemporaryFile()
                        temp_pdf_file.write(data['pdf'])
                        pdf_metadata = self.get_pdf_metadata(temp_pdf_file)
                        temp_pdf_file.close()

                        data = dict(data, **pdf_metadata)
                    else:
                        data['error'] = self.tr('Unknown Content-Type')
                        self.log(self.tr('Failed to get PDF!'), 'ERROR')
                        self.log(data['error'], 'ERROR')
                except Exception as err:
                    data['error'] = str(err)
                    self.log(self.tr('Failed to get PDF!'), 'ERROR')
                    self.log(data['error'], 'ERROR')

            if not 'error' in data:
                break
            else:
                if round == len(scihub_available_urls_) - 1:
                    self.log(self.tr('Failed with all Sci-Hub URLs!'), 'ERROR')
                else:
                    self.log(self.tr('Changing Sci-Hub URL ...'), 'INFO')

        return data

    def rampage(self, query):
        self.log('\n')
        log_formater = self.tr('Dealing with query: ') + '{query}'
        self.log(log_formater.format(query=query), 'INFO')

        data = self.fetch(query)

        if not 'error' in data:
            pdf_name_formater = self._conf.get('common', 'filename_prefix_format') + '_{filename}'
            pdf_name = pdf_name_formater.format(**data)
            pdf_path = os.path.join(self._conf.get('common', 'save_to_dir'), pdf_name)

            with open(pdf_path, 'wb') as fp:
                fp.write(data['pdf'])

            log_formater = self.tr('Saved PDF as: ') + '{pdf_name}'
            self.log(log_formater.format(pdf_name=pdf_name), 'INFO')

    def run(self):
        self.rampage(self._query)

        if self._callback:
            self._callback()


if __name__ == '__main__':
    pass
