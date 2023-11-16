import logging
from typing import List

from decouple import config

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
BOT_DOWNLOAD_FOLDER_PATH: str = config('BOT_DOWNLOAD_FOLDER_PATH', default=None, cast=str)

# comma separated list of arguments (ex: --headless, --disable-gui)
FIREFOX_ARGUMENTS: List[str] = config('FIREFOX_ARGUMENTS', default=[])

FIREFOX_USER_AGENT: str = config('FIREFOX_USER_AGENT', default=f'{PROJECT_NAME} {APP_VERSION}', cast=str)

FIREFOX_PROXY_ENABLED: bool = config('FIREFOX_PROXY_ENABLED', default=False, cast=bool)
FIREFOX_HTTP_PROXY: str = config('FIREFOX_HTTP_PROXY', default=None, cast=str)
FIREFOX_HTTPS_PROXY: str = config('FIREFOX_HTTPS_PROXY', default=FIREFOX_HTTP_PROXY, cast=str)

FIREFOX_SCREENSHOT_DOWNLOAD_FOLDER_PATH: str = config('FIREFOX_SCREENSHOT_DOWNLOAD_FOLDER_PATH', default='debug/', cast=str)
FIREFOX_HTML_DOWNLOAD_FOLDER_PATH: str = config('FIREFOX_HTML_DOWNLOAD_FOLDER_PATH', default='debug/', cast=str)
FIREFOX_COOKIES_FILE: str = config('FIREFOX_COOKIES_FILE_PATH', default='cookies.pkl', cast=str)

FIREFOX_PREFERENCES_FILE_PATH: str = config('FIREFOX_PREFERENCES_FILE_PATH', default='firefox_preferences.json', cast=str)

# selenium
SELENIUM_GLOBAL_IMPLICIT_WAIT: int = config('SELENIUM_GLOBAL_IMPLICIT_WAIT', default=5, cast=int)
SELENIUM_EXPECTED_URL_TIMEOUT: int = config('SELENIUM_EXPECTED_URL_TIMEOUT', default=5, cast=int)
SELENIUM_DEFAULT_WAIT: int = config('SELENIUM_DEFAULT_WAIT', default=5, cast=int)
SELENIUM_LOCATORS_FILE: str = config('SELENIUM_LOCATORS_FILE', default='locators.ini', cast=str)