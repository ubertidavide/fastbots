import tempfile
import shutil
import pickle
from typing import List, Union
from pathlib import Path
from datetime import datetime
import configparser
import logging
from typing import Type
from abc import ABC, abstractmethod

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

from fastbots import config
from fastbots.exceptions import ExpectedUrlError


logger = logging.getLogger(__name__)


class Bot(ABC):
    """
    Bot

    Class used to specify a bot blueprint.
    """

    def __init__(self) -> None:
        """
        Bot

        Initialize all the attributes of the Bot instance
        """
        super().__init__()

        # use a temporary directory as default download folder
        if config.BOT_DOWNLOAD_FOLDER_PATH != 'None':
            self._temp_dir: str = tempfile.mkdtemp(dir=config.BOT_DOWNLOAD_FOLDER_PATH)
        else:
            self._temp_dir: str = tempfile.mkdtemp()

        # load all the locators
        self._locators: configparser = self.__load_locators__()
        # data store
        self._payload: dict = {}

    @property
    def driver(self) -> webdriver:
        """
        Driver Getter
        """
        return self._driver
    
    @property
    def wait(self) -> WebDriverWait:
        """
        Wait Getter
        """
        return self._wait
    
    @property
    def payload(self) -> dict:
        """
        Payload Getter
        """
        return self._payload

    def __enter__(self) -> Type['Bot']:
        """
        Enter

        Load and configure all the needed resources.
        """
        # default global driver settings
        self._driver.implicitly_wait(config.SELENIUM_GLOBAL_IMPLICIT_WAIT)

        # load the start page
        self._driver.get(self.locator('pages_url', 'start_url'))

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Exit
        
        Clean all the used resources.
        """
        shutil.rmtree(self._temp_dir)
        self._driver.close()

    def check_page_url(self, expected_page_url: str):
        """
        Check Page Url

        Check that the browser it't at the expected page.
        """
        try:
            # polling that the page url is the expected
            WebDriverWait(driver=self._driver, timeout=config.SELENIUM_EXPECTED_URL_TIMEOUT, poll_frequency=1).until(
                EC.url_to_be(expected_page_url)
            )

        except TimeoutException as te:
            # if not the expected url raises an exception
            raise ExpectedUrlError(current_url=self._driver.current_url, expected_url=expected_page_url)

    def locator(self, page_name: str, locator_name: str) -> str:
        """
        Locator

        Getter that get the locator used for a page locator
        """
        if not self._locators.has_section(page_name):
            raise ValueError(f'The specified page_name: {page_name} is not declared in locators config.')
        if not self._locators.has_option(locator_name):
            raise ValueError(f'The specified locator_name: {locator_name} is not declared in locators config.')
        return self._locators.get(page_name, locator_name)
        
    def save_screenshot(self):
        """
        Save Screenshot

        Save the browser's screenshot to a png file, the path could be specified in the settings.
        """
        if not Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).exists():
            Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).mkdir(exist_ok=True, parents=True)

        file_path: Path = Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH) / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
        self._driver.save_screenshot(str(file_path.absolute()))

    def save_html(self):
        """
        Save Html

        Save the browser's html page to a file, the path could be specified in the settings.
        """
        if not Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH).exists():
            Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH).mkdir(exist_ok=True, parents=True)

        file_path: Path = Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH) / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.html'
        with open(str(file_path.absolute()), "w", encoding="utf-8") as file:
            file.write(self._driver.page_source)

    def save_cookies(self):
        """
        Save Cookies

        Save all the cookies founded in the file.
        """
        cookies: List[dict] = self._driver.get_cookies()

        with open(config.BOT_COOKIES_FILE_PATH, 'wb') as file:
            pickle.dump(cookies, file)
    
    def load_cookies(self):
        """
        Load Cookies

        Add all the cookies founded in the file.
        """
        if Path(config.BOT_COOKIES_FILE_PATH).is_file():
            with open(config.BOT_COOKIES_FILE_PATH, 'rb') as file:
                cookies = pickle.load(file)

                for cookie in cookies:
                    self._driver.add_cookie(cookie)

    def __load_locators__(self) -> configparser:
        """
        Load Locators

        Load a file that contains all the locators
        """
        if not Path(config.SELENIUM_LOCATORS_FILE).is_file():
            return ValueError(f'Erorr, locators file not founded at path: {config.SELENIUM_LOCATORS_FILE}')
        
        config_parser: configparser = configparser.ConfigParser()
        config_parser.read(config.SELENIUM_LOCATORS_FILE)
        return config_parser

    @abstractmethod
    def __load_preferences__(self) -> Union[FirefoxProfile, dict]:
        """
        Load Preferences

        Load all the preferences stored in a json file,
        specified in the config.
        """
        return NotImplementedError('Bot must define this method.')

    @abstractmethod
    def __load_options__(self) -> Union[FirefoxOptions, ChromeOptions]:
        """
        Load Options

        Load all the default options
        """
        return NotImplementedError('Bot must define this method.')
    
    @abstractmethod
    def __load_driver__(self) -> webdriver:
        """
        Load Driver

        Load and configure all the options for the driver.
        """
        return NotImplementedError('Bot must define this method.')