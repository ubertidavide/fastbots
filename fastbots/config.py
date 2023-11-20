import logging
from typing import List
from enum import Enum

from decouple import config


class DriverType(Enum):
    FIREFOX = 1
    CHROME = 2

# static config
ENV_DEVELOPMENT: str = 'development'
ENV_RELEASE: str = 'release'

# dynamic config

# project settings
LOG_LEVEL: int = config('LOGLEVEL', default=logging.DEBUG, cast=int)
ENV: str = config('ENV', default=ENV_DEVELOPMENT, cast=str)

PROJECT_NAME: str = config('PROJECT_NAME', default='fastbot', cast=str)
APP_VERSION: str = config('APP_VERSION', default='0.1.0', cast=str)

# firefox settings
BOT_DRIVER_TYPE: DriverType = config('BOT_DRIVER_TYPE', default=DriverType.FIREFOX, cast=DriverType)
BOT_DOWNLOAD_FOLDER_PATH: str = config('BOT_DOWNLOAD_FOLDER_PATH', default=None, cast=str)

# comma separated list of arguments (ex: --headless, --disable-gui)
BOT_ARGUMENTS: List[str] = config('BOT_ARGUMENTS', default=[])

BOT_USER_AGENT: str = config('BOT_USER_AGENT', default=f'{PROJECT_NAME} {APP_VERSION}', cast=str)

BOT_PROXY_ENABLED: bool = config('BOT_PROXY_ENABLED', default=False, cast=bool)
BOT_HTTP_PROXY: str = config('BOT_HTTP_PROXY', default=None, cast=str)
BOT_HTTPS_PROXY: str = config('BOT_HTTPS_PROXY', default=BOT_HTTP_PROXY, cast=str)

BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH: str = config('BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH', default='debug/', cast=str)
BOT_HTML_DOWNLOAD_FOLDER_PATH: str = config('BOT_HTML_DOWNLOAD_FOLDER_PATH', default='debug/', cast=str)
BOT_COOKIES_FILE_PATH: str = config('BOT_COOKIES_FILE_PATH', default='cookies.pkl', cast=str)

BOT_PREFERENCES_FILE_PATH: str = config('BOT_PREFERENCES_FILE_PATH', default='preferences.json', cast=str)

BOT_MAX_RETRIES: int = config('BOT_MAX_RETRIES', default=2, cast=int)
BOT_RETRY_DELAY: int = config('BOT_RETRY_DELAY', default=10, cast=int)

# selenium
SELENIUM_GLOBAL_IMPLICIT_WAIT: int = config('SELENIUM_GLOBAL_IMPLICIT_WAIT', default=5, cast=int)
SELENIUM_EXPECTED_URL_CHECK: bool = config('SELENIUM_EXPECTED_URL_CHECK', default=True, cast=bool)
SELENIUM_EXPECTED_URL_TIMEOUT: int = config('SELENIUM_EXPECTED_URL_TIMEOUT', default=5, cast=int)
SELENIUM_DEFAULT_WAIT: int = config('SELENIUM_DEFAULT_WAIT', default=5, cast=int)
SELENIUM_FILE_DOWNLOAD_TIMEOUT: int = config('SELENIUM_FILE_DOWNLOAD_TIMEOUT', default=20, cast=int)
SELENIUM_LOCATORS_FILE: str = config('SELENIUM_LOCATORS_FILE', default='locators.ini', cast=str)