```python
import logging
from enum import Enum

from decouple import config

# Define an enumeration for driver types
class DriverType(Enum):
    FIREFOX = 1
    CHROME = 2

# Define static configurations

# Possible values: 'development' or 'release'
ENV_DEVELOPMENT: str = 'development'
ENV_RELEASE: str = 'release'

# Dynamic configurations

# Logging level for the application
# Possible values: logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
LOG_LEVEL: int = config('LOGLEVEL', default=logging.DEBUG, cast=int)

# Environment type
# Possible values: 'development' or 'release'
ENV: str = config('ENV', default=ENV_DEVELOPMENT, cast=str)

# Project information
PROJECT_NAME: str = config('PROJECT_NAME', default='fastbot', cast=str)
APP_VERSION: str = config('APP_VERSION', default='0.1.0', cast=str)

# WebDriver settings for bot

# Driver type for the bot
# Possible values: DriverType.FIREFOX or DriverType.CHROME
BOT_DRIVER_TYPE: DriverType = config('BOT_DRIVER_TYPE', default=DriverType.FIREFOX, cast=DriverType)

# Path to the download folder for the bot
# Set to None for the default temporary directory
BOT_DOWNLOAD_FOLDER_PATH: str = config('BOT_DOWNLOAD_FOLDER_PATH', default=None, cast=str)
# Move to the download folder only waited download files, it require the usage of the appostie function for download wait
BOT_STRICT_DOWNLOAD_WAIT: bool = config('BOT_STRICT_DOWNLOAD_WAIT', default=True, cast=bool)

# Comma-separated list of additional arguments for the bot
BOT_ARGUMENTS: str = config('BOT_ARGUMENTS', default=None, cast=str)

# User agent string for the bot
BOT_USER_AGENT: str = config('BOT_USER_AGENT', default=f'{PROJECT_NAME} {APP_VERSION}', cast=str)

# Proxy settings for the bot
BOT_PROXY_ENABLED: bool = config('BOT_PROXY_ENABLED', default=False, cast=bool)
BOT_HTTP_PROXY: str = config('BOT_HTTP_PROXY', default=None, cast=str)
BOT_HTTPS_PROXY: str = config('BOT_HTTPS_PROXY', default=BOT_HTTP_PROXY, cast=str)

# Paths for storing screenshots, HTML pages, and cookies
BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH: str = config('BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH', default='debug/', cast=str)
BOT_HTML_DOWNLOAD_FOLDER_PATH: str = config('BOT_HTML_DOWNLOAD_FOLDER_PATH', default='debug/', cast=str)
BOT_COOKIES_FILE_PATH: str = config('BOT_COOKIES_FILE_PATH', default='cookies.pkl', cast=str)

# Path to the preferences file for Firefox bot
BOT_PREFERENCES_FILE_PATH: str = config('BOT_PREFERENCES_FILE_PATH', default='preferences.json', cast=str)

# Bot retry settings
BOT_MAX_RETRIES: int = config('BOT_MAX_RETRIES', default=2, cast=int)
BOT_RETRY_DELAY: int = config('BOT_RETRY_DELAY', default=10, cast=int)

# Selenium configurations

# Global implicit wait time for the Selenium driver
SELENIUM_GLOBAL_IMPLICIT_WAIT: int = config('SELENIUM_GLOBAL_IMPLICIT_WAIT', default=5, cast=int)

# Check if the expected URL should be verified
SELENIUM_EXPECTED_URL_CHECK: bool = config('SELENIUM_EXPECTED_URL_CHECK', default=True, cast=bool)

# Timeout for checking the expected URL
SELENIUM_EXPECTED_URL_TIMEOUT: int = config('SELENIUM_EXPECTED_URL_TIMEOUT', default=5, cast=int)

# Default wait time for Selenium actions
SELENIUM_DEFAULT_WAIT: int = config('SELENIUM_DEFAULT_WAIT', default=5, cast=int)

# Timeout for waiting for file downloads in Selenium
SELENIUM_FILE_DOWNLOAD_TIMEOUT: int = config('SELENIUM_FILE_DOWNLOAD_TIMEOUT', default=20, cast=int)

# Path to the locators file for Selenium
SELENIUM_LOCATORS_FILE: str = config('SELENIUM_LOCATORS_FILE', default='locators.ini', cast=str)

```