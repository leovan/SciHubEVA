import logging
import threading
import time
from enum import Enum, unique
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Callable
from urllib.parse import urlparse

from lxml import etree
from pathvalidate import sanitize_filename
from PySide6.QtCore import QObject
from requests import Session

from scihub_eva.globals.preferences import *
from scihub_eva.utils.api_utils import *
from scihub_eva.utils.logging_utils import *
from scihub_eva.utils.preferences_utils import *


@unique
class SciHubAPIRampageType(Enum):
    # Raw query
    RAW = 0

    # Query with captcha
    WITH_CAPTCHA = 1


@unique
class SciHubAPIError(Enum):
    # Unknown error
    UNKNOWN = 0

    # Cannot find a valid PDF when fetching PDF URL
    NO_VALID_PDF = 1

    # Cannot download automatically due to captcha
    BLOCKED_BY_CAPTCHA = 2

    # Wrong captcha
    WRONG_CAPTCHA = 3


class SciHubAPI(QObject, threading.Thread):
    def __init__(
        self,
        logger: logging.Logger,
        callback: Callable[[str, Any, Any], None],
        scihub_url: str,
        sess: Session,
        raw_query: str | None = None,
        query: str | None = None,
        rampage_type: Any | None = None,
    ) -> None:
        QObject.__init__(self)
        threading.Thread.__init__(self)

        self._logger = logger
        self._callback = callback

        self._scihub_url = scihub_url
        self._sess = sess
        self._raw_query = raw_query
        self._query = query
        self._rampage_type = rampage_type
        self._captcha_answer: str | None = None

    def __del__(self) -> None:
        self._sess.close()

    @property
    def raw_query(self) -> str | None:
        return self._raw_query

    @raw_query.setter
    def raw_query(self, raw_query: str) -> None:
        self._raw_query = raw_query

    @property
    def query(self) -> str | None:
        return self._query

    @query.setter
    def query(self, query: str) -> None:
        self._query = query

    @property
    def rampage_type(self) -> str | None:
        return self._rampage_type

    @rampage_type.setter
    def rampage_type(self, rampage_type: str) -> None:
        self._rampage_type = rampage_type

    @property
    def captcha_answer(self) -> str | None:
        return self._captcha_answer

    @captcha_answer.setter
    def captcha_answer(self, captcha_answer: str | None) -> None:
        self._captcha_answer = captcha_answer

    def fetch_pdf_url(self, query: str) -> tuple[Any, Any]:
        self._logger.info(
            self.tr('Using Sci-Hub URL: ')
            + f'<a href="{self._scihub_url}">{self._scihub_url}</a>'
        )

        query_type = guess_query_type(query)
        self._logger.info(self.tr('Query type: ') + query_type.upper())

        pdf_url = query
        err = None

        if query_type != 'pdf':
            try:
                self._logger.info(self.tr('Fetching PDF URL ...'))

                pdf_url_response = self._sess.post(
                    self._scihub_url,
                    data={'request': query},
                    verify=False,
                    timeout=Preferences.get_or_default(
                        NETWORK_TIMEOUT_KEY, NETWORK_RETRY_TIMES_DEFAULT, value_type=int
                    )
                    / 1000.0,
                )

                if pdf_url_response.status_code != 200:
                    self._logger.error(
                        self.tr('Error {}').format(pdf_url_response.status_code)
                    )
                    self._logger.info(self.tr('You may need check it manually.'))
                    err = SciHubAPIError.UNKNOWN
                else:
                    html = etree.HTML(pdf_url_response.content)
                    pdf_xpath_list = Preferences.get_or_default(
                        API_PDF_XPATHS_KEY, API_PDF_XPATHS_DEFAULT, value_type=list
                    )

                    pdfs = []
                    for pdf_xpath in pdf_xpath_list:
                        results = html.xpath(pdf_xpath) if html is not None else None

                        if results and len(results) > 0:
                            pdfs.extend(results)

                    if pdfs and len(pdfs) > 0:
                        pdf_url = urlparse(pdfs[0].attrib['src'])
                        response_url = urlparse(pdf_url_response.url)

                        if pdf_url.scheme == '':
                            pdf_url = pdf_url._replace(scheme=response_url.scheme)

                        if pdf_url.netloc == '':
                            pdf_url = pdf_url._replace(netloc=response_url.netloc)

                        pdf_url = pdf_url.geturl()
                        pdf_url_html = f'<a href="{pdf_url}">{pdf_url}</a>'

                        self._logger.info(self.tr('Got PDF URL: ') + pdf_url_html)
                    else:
                        err = SciHubAPIError.NO_VALID_PDF

                        self._logger.error(self.tr('Failed to get PDF URL!'))
                        self._logger.info(self.tr('You may need check it manually.'))
            except Exception as e:
                err = SciHubAPIError.UNKNOWN

                self._logger.error(self.tr('Failed to get PDF URL!'))
                self._logger.info(self.tr('You may need check it manually.'))
                self._logger.error(str(e))

        return pdf_url, err

    def get_captcha_info(self, pdf_captcha_response: Any) -> tuple[Any, Any]:
        captcha_id, captcha_img_url = None, None

        html = etree.HTML(pdf_captcha_response.content)

        captcha_id_xpath_list = Preferences.get_or_default(
            API_CAPTCHA_ID_XPATHS_KEY, API_CAPTCHA_ID_XPATHS_DEFAULT, value_type=list
        )
        captcha_image_xpath_list = Preferences.get_or_default(
            API_CAPTCHA_IMAGE_XPATHS_KEY,
            API_CAPTCHA_IMAGE_XPATHS_DEFAULT,
            value_type=list,
        )

        captcha_ids = []
        for captcha_id_xpath in captcha_id_xpath_list:
            results = html.xpath(captcha_id_xpath) if html is not None else None

            if results and len(results) > 0:
                captcha_ids.extend(results)

        captcha_images = []
        for captcha_image_xpath in captcha_image_xpath_list:
            results = html.xpath(captcha_image_xpath) if html is not None else None

            if results and len(results) > 0:
                captcha_images.extend(results)

        if len(captcha_images) > 0 and len(captcha_ids) > 0:
            captcha_id = captcha_ids[0].attrib['value']
            captcha_img_url = urlparse(captcha_images[0].attrib['src'])
            response_url = urlparse(pdf_captcha_response.url)

            if captcha_img_url.scheme == '':
                captcha_img_url = captcha_img_url._replace(scheme=response_url.scheme)

            if captcha_img_url.netloc == '':
                captcha_img_url = captcha_img_url._replace(netloc=response_url.netloc)

            captcha_img_url = captcha_img_url.geturl()

        return captcha_id, captcha_img_url

    def download_captcha_img(self, captcha_img_url: str) -> Path:
        captcha_img_file = NamedTemporaryFile(delete=False)
        captcha_img_file_path = Path(captcha_img_file.name)

        captcha_img_res = self._sess.get(captcha_img_url, stream=True)

        if captcha_img_res.status_code == 200:
            for chuck in captcha_img_res:
                captcha_img_file.write(chuck)

        captcha_img_file.flush()
        captcha_img_file.close()

        return captcha_img_file_path

    def fetch_pdf_with_captcha(self, pdf_captcha_response: Any) -> tuple[Any, Any]:
        pdf, err = None, None

        captcha_id, _ = self.get_captcha_info(pdf_captcha_response)

        pdf_response = self._sess.post(
            pdf_captcha_response.url,
            data={'answer': self._captcha_answer, 'id': captcha_id},
            verify=False,
            timeout=Preferences.get_or_default(
                NETWORK_TIMEOUT_KEY, NETWORK_RETRY_TIMES_DEFAULT, value_type=int
            )
            / 1000.0,
        )

        if pdf_response.status_code != 200:
            self._logger.error(self.tr('Error {}').format(pdf_response.status_code))
            self._logger.info(self.tr('You may need check it manually.'))
            err = SciHubAPIError.UNKNOWN
        elif pdf_response.headers['Content-Type'] == 'application/pdf':
            self._logger.info(self.tr('Angel [CAPTCHA] down!'))
            pdf = pdf_response.content
        else:
            pdf = pdf_response
            err = SciHubAPIError.WRONG_CAPTCHA

        return pdf, err

    def fetch_pdf(self, pdf_url: str) -> tuple[Any, Any]:
        self._logger.info(self.tr('Fetching PDF ...'))

        pdf, err = None, None

        try:
            pdf_response = self._sess.get(
                pdf_url,
                verify=False,
                timeout=Preferences.get_or_default(
                    NETWORK_TIMEOUT_KEY, NETWORK_RETRY_TIMES_DEFAULT, value_type=int
                )
                / 1000.0,
            )

            if pdf_response.status_code != 200:
                self._logger.error(self.tr('Error {}').format(pdf_response.status_code))
                self._logger.info(self.tr('You may need check it manually.'))
                err = SciHubAPIError.UNKNOWN
            elif pdf_response.headers['Content-Type'] == 'application/pdf':
                pdf = pdf_response.content
            elif pdf_response.headers['Content-Type'].startswith('text/html'):
                self._logger.warn(self.tr('Angel [CAPTCHA] is coming!'))
                err = SciHubAPIError.BLOCKED_BY_CAPTCHA
                pdf = pdf_response
            else:
                self._logger.error(self.tr('Unknown PDF Content-Type!'))
                self._logger.info(self.tr('You may need check it manually.'))
        except Exception as e:
            err = SciHubAPIError.UNKNOWN

            self._logger.error(self.tr('Failed to get PDF!'))
            self._logger.info(self.tr('You may need check it manually.'))
            self._logger.error(str(e))

        return pdf, err

    def save_pdf(self, pdf: Any, filename: str) -> None:
        pdf_name_formatter = Preferences.get_or_default(
            FILE_FILENAME_PREFIX_FORMAT_KEY, FILE_FILENAME_PREFIX_FORMAT_DEFAULT
        )

        if not Preferences.get_or_default(
            FILE_OVERWRITE_EXISTING_FILE_KEY,
            FILE_OVERWRITE_EXISTING_FILE_DEFAULT,
            value_type=bool,
        ):
            pdf_name_formatter += '_' + str(round(time.time() * 1000000))

        pdf_metadata = get_pdf_metadata(pdf)
        query_type = guess_query_type(self._raw_query)

        if query_type in ['doi', 'pmid']:
            pdf_metadata['id'] = self._raw_query
        else:
            for patten in ['_{id}', '{id}_', '{id}']:
                pdf_name_formatter = pdf_name_formatter.replace(patten, '')

        pdf_name_formatter += '_' + filename if pdf_name_formatter else filename

        try:
            pdf_name = pdf_name_formatter.format(**pdf_metadata)
        except Exception:
            self._logger.error(
                self.tr('Unsupported filename keywords: ') + pdf_name_formatter
            )
            return

        pdf_name = sanitize_filename(pdf_name, replacement_text='-')
        pdf_path = Path(Preferences.get(FILE_SAVE_TO_DIR_KEY)) / pdf_name

        with open(pdf_path, 'wb') as fp:
            fp.write(pdf)

        pdf_link = f'<a href="{pdf_path.as_uri()}">{pdf_path.as_posix()}</a>'

        self._logger.info(self.tr('Saved PDF as: ') + pdf_link)

    def rampage(self, query: str, rampage_type: str) -> tuple[Any, Any]:
        if rampage_type == SciHubAPIRampageType.RAW:
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
        elif rampage_type == SciHubAPIRampageType.WITH_CAPTCHA:
            # Fetch PDF with Captcha
            pdf, err = self.fetch_pdf_with_captcha(query)
            if err == SciHubAPIError.WRONG_CAPTCHA:
                self._logger.error(
                    self.tr('Wrong captcha, failed to kill Angel [CAPTCHA]!')
                )
                return None, err

            # Save PDF
            filename = urlparse(query.url).path[1:].split('/')[-1]
            self.save_pdf(pdf, filename)

        return None, None

    def run(self) -> None:
        res, err = self.rampage(self._query, self._rampage_type)
        self._callback(self._raw_query, res, err)


__all__ = ['SciHubAPIRampageType', 'SciHubAPIError', 'SciHubAPI']
