import urllib3
from requests import Session
from requests.adapters import HTTPAdapter

from scihub_eva.globals.preferences import *
from scihub_eva.utils.preferences_utils import Preferences

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_max_retries_adapter() -> HTTPAdapter:
    retry_times = Preferences.get_or_default(
        NETWORK_RETRY_TIMES_KEY, NETWORK_RETRY_TIMES_DEFAULT, value_type=int
    )
    return HTTPAdapter(max_retries=retry_times)


def get_proxies() -> dict[str, str]:
    proxy_type = Preferences.get_or_default(
        NETWORK_PROXY_TYPE_KEY, NETWORK_PROXY_TYPE_DEFAULT
    )
    proxy_host = Preferences.get_or_default(
        NETWORK_PROXY_HOST_KEY, NETWORK_PROXY_HOST_DEFAULT
    )
    proxy_port = Preferences.get_or_default(
        NETWORK_PROXY_PORT_KEY, NETWORK_PROXY_PORT_DEFAULT
    )
    proxy_username = Preferences.get_or_default(
        NETWORK_PROXY_USERNAME_KEY, NETWORK_PROXY_USERNAME_DEFAULT
    )
    proxy_password = Preferences.get_or_default(
        NETWORK_PROXY_PASSWORD_KEY, NETWORK_PROXY_PASSWORD_DEFAULT
    )

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


def get_default_headers(ua: str) -> dict[str, str]:
    return {
        'User-Agent': ua,
        'Accept': 'text/html',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
        'DNT': '1',
    }


def get_session(scihub_url: str) -> Session:
    sess = Session()

    max_retries_adapter = get_max_retries_adapter()
    sess.mount(prefix='http://', adapter=max_retries_adapter)
    sess.mount(prefix='https://', adapter=max_retries_adapter)

    proxy_enabled = Preferences.get_or_default(
        NETWORK_PROXY_ENABLE_KEY, NETWORK_PROXY_ENABLE_DEFAULT, value_type=bool
    )

    if proxy_enabled:
        sess.proxies = get_proxies()

    ua = Preferences.get_or_default(NETWORK_USER_AGENT_KEY, NETWORK_USER_AGENT_DEFAULT)
    sess.headers = get_default_headers(ua)

    return sess


__all__ = ['get_session']
