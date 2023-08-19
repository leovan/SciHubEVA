# -*- coding: utf-8 -*-

import requests

from requests.adapters import HTTPAdapter

from scihub_eva.utils.preferences_utils import Preferences
from scihub_eva.globals.preferences import *


def get_session():
    sess = requests.Session()
    sess.headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/115.0.0.0 '
            'Safari/537.36'
    }

    retry_times = Preferences.get_or_default(
        NETWORK_RETRY_TIMES_KEY, NETWORK_RETRY_TIMES_DEFAULT, type=int)
    adapter = HTTPAdapter(max_retries=retry_times)

    sess.mount('http://', adapter)
    sess.mount('https://', adapter)

    proxy_enabled = Preferences.get_or_default(
        NETWORK_PROXY_ENABLE_KEY, NETWORK_PROXY_ENABLE_DEFAULT, type=bool)

    if proxy_enabled:
        proxy_type = Preferences.get_or_default(
            NETWORK_PROXY_TYPE_KEY, NETWORK_PROXY_TYPE_DEFAULT)
        proxy_host = Preferences.get_or_default(
            NETWORK_PROXY_HOST_KEY, NETWORK_PROXY_HOST_DEFAULT)
        proxy_port = Preferences.get_or_default(
            NETWORK_PROXY_PORT_KEY, NETWORK_PROXY_PORT_DEFAULT)
        proxy_username = Preferences.get_or_default(
            NETWORK_PROXY_USERNAME_KEY, NETWORK_PROXY_USERNAME_DEFAULT)
        proxy_password = Preferences.get_or_default(
            NETWORK_PROXY_PASSWORD_KEY, NETWORK_PROXY_PASSWORD_DEFAULT)

        proxy = proxy_type + '://'

        if proxy_username and proxy_username != '':
            proxy += proxy_username

        if proxy_password and proxy_password != '':
            proxy += ':' + proxy_password

        if proxy_username and proxy_username != '':
            proxy += '@'

        proxy += proxy_host

        if proxy_port and proxy_port != '':
            proxy += ':' + proxy_port

        sess.proxies = {'http': proxy, 'https': proxy}

    return sess


__all__ = [
    'get_session'
]
