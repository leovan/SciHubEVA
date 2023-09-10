# -*- coding: utf-8 -*-

import re
import json
import urllib3

from requests import Response, Session, cookies
from requests.adapters import HTTPAdapter

from scihub_eva.utils.preferences_utils import Preferences
from scihub_eva.utils.path_utils import *
from scihub_eva.globals.preferences import *


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_adapter():
    retry_times = Preferences.get_or_default(
        NETWORK_RETRY_TIMES_KEY, NETWORK_RETRY_TIMES_DEFAULT, type=int)
    return HTTPAdapter(max_retries=retry_times)


def get_proxies():
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

    return {'http': proxy, 'https': proxy}


def get_default_headers(ua):
    return {
        'User-Agent': Preferences.get_or_default(
            NETWORK_USER_AGENT_KEY, NETWORK_USER_AGENT_DEFAULT),
        'Accept': 'text/html',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
        'DNT': '1'
    }


def set_cookies(sess: Session, resp: Response):
    for k, v in resp.cookies.items():
        sess.cookies.set_cookie(cookies.create_cookie(k, v))


def ddos_guard_bypass(url, sess: Session):
    url = re.sub('/+$', '', url)
    check_resp = sess.get(url)

    if (check_resp.status_code == 403
            or check_resp.headers.get('server', '').lower() == 'ddos-guard'):
        set_cookies(sess, check_resp)
    else:
        return

    guard_resp = sess.get(f'{url}/.well-known/ddos-guard/check?context=free_splash')
    if guard_resp.status_code != 200:
        return
    else:
        set_cookies(sess, guard_resp)

    with open((CONFS_DIR / 'ddos-guard-fake-mark.json').resolve().as_posix()) as f:
        fake_mark = json.load(f)

    mark_resp = sess.post(f'{url}/.well-known/ddos-guard/mark/', json=fake_mark)
    if mark_resp != 200:
        return
    else:
        set_cookies(sess, mark_resp)

    url = re.sub('/+$', '', url)
    check_resp = sess.get(url)
    if check_resp.status_code != 403:
        set_cookies(sess, check_resp)


def get_session(scihub_url):
    sess = Session()

    adapter = get_adapter()
    sess.mount(prefix='http://', adapter=adapter)
    sess.mount(prefix='https://', adapter=adapter)

    proxy_enabled = Preferences.get_or_default(
        NETWORK_PROXY_ENABLE_KEY, NETWORK_PROXY_ENABLE_DEFAULT, type=bool)

    if proxy_enabled:
        sess.proxies = get_proxies()

    ua = Preferences.get_or_default(
        NETWORK_USER_AGENT_KEY, NETWORK_USER_AGENT_DEFAULT)
    sess.headers = get_default_headers(ua)

    ddos_guard_bypass(scihub_url, sess)

    return sess


__all__ = [
    'get_session'
]
