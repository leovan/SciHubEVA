# -*- coding: utf-8 -*-

# System
SYSTEM_LANGUAGE_KEY = 'System/Language'

SYSTEM_THEME_KEY = 'System/Theme'
SYSTEM_THEME_DEFAULT = 'System'

# File
FILE_SAVE_TO_DIR_KEY = 'File/SaveToDir'
FILE_SAVE_TO_DIR_DEFAULT = ''

FILE_FILENAME_PREFIX_FORMAT_KEY = 'File/FilenamePrefixFormat'
FILE_FILENAME_PREFIX_FORMAT_DEFAULT = '{id}_{year}_{author}_{title}'

FILE_OVERWRITE_EXISTING_FILE_KEY = 'File/OverwriteExistingFile'
FILE_OVERWRITE_EXISTING_FILE_DEFAULT = False

# Network
NETWORK_SCIHUB_URL_KEY = 'Network/SciHubURL'
NETWORK_SCIHUB_URL_DEFAULT = 'https://sci-hub.se'

NETWORK_SCIHUB_URLS_KEY = 'Network/SciHubURLs'
NETWORK_SCIHUB_URLS_DEFAULT = [
    'https://sci-hub.se',
    'https://sci-hub.st',
    'https://sci-hub.ru',
]

NETWORK_TIMEOUT_KEY = 'Network/Timeout'
NETWORK_TIMEOUT_DEFAULT = 3000

NETWORK_RETRY_TIMES_KEY = 'Network/RetryTimes'
NETWORK_RETRY_TIMES_DEFAULT = 3

NETWORK_USER_AGENT_KEY = 'Network/UserAgent'
NETWORK_USER_AGENT_DEFAULT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
        'AppleWebKit/537.36 (KHTML, like Gecko) ' +
        'Chrome/116.0.0.0 ' +
        'Safari/537.36'
)

NETWORK_PROXY_ENABLE_KEY = 'Network/ProxyEnable'
NETWORK_PROXY_ENABLE_DEFAULT = False

NETWORK_PROXY_TYPE_KEY = 'Network/ProxyType'
NETWORK_PROXY_TYPE_DEFAULT = 'http'

NETWORK_PROXY_HOST_KEY = 'Network/ProxyHost'
NETWORK_PROXY_HOST_DEFAULT = '127.0.0.1'

NETWORK_PROXY_PORT_KEY = 'Network/ProxyPort'
NETWORK_PROXY_PORT_DEFAULT = '7890'

NETWORK_PROXY_USERNAME_KEY = 'Network/ProxyUsername'
NETWORK_PROXY_USERNAME_DEFAULT = ''

NETWORK_PROXY_PASSWORD_KEY = 'Network/ProxyPassword'
NETWORK_PROXY_PASSWORD_DEFAULT = ''
