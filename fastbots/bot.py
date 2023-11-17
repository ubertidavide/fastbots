import tempfile
import json
import shutil
import pickle
from typing import List
from pathlib import Path
from datetime import datetime
import configparser
import logging

from seleniumwire.webdriver import Firefox, Chrome
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

from fastbots import config, logger
from fastbots.exceptions import ExpectedUrlError


logger = logging.getLogger(__name__)


class Bot(object):
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

        # variable instanciated at enter
        if config.BOT_DRIVER_TYPE == config.DriverType.FIREFOX:
            self._driver: webdriver = self.__load_firefox_driver__()
        elif config.BOT_DRIVER_TYPE == config.DriverType.CHROME:
            self._driver: webdriver = self.__load_chrome_driver__()
        else:
            raise ValueError('Unknown driver type selected')
        
        # default wait
        self._wait: WebDriverWait = WebDriverWait(driver=self._driver, timeout=config.SELENIUM_DEFAULT_WAIT, poll_frequency=1)
        # data store
        self._payload: dict = {}

    @property
    def driver(self):
        """
        Driver Getter
        """
        return self._driver
    
    @property
    def wait(self):
        """
        Wait Getter
        """
        return self._wait
    
    @property
    def payload(self):
        """
        Payload Getter
        """
        return self._payload

    def __enter__(self):
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

    def locator(self, page_name: str, locator_name: str):
        """
        Locator

        Getter that get the locator used for a page locator
        """
        return self._locators.get(page_name, locator_name)
        
    def save_screenshot(self):
        """
        Save Screenshot

        Save the browser's screenshot to a png file, the path could be specified in the settings.
        """
        if not Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).exists():
            Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).mkdir(exist_ok=True, parents=True)

        file_path: Path = Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH) / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'

        if config.BOT_DRIVER_TYPE == config.DriverType.FIREFOX:
            self._driver.get_full_page_screenshot_as_file(str(file_path.absolute()))
        elif config.BOT_DRIVER_TYPE == config.DriverType.CHROME:
            self._driver.save_screenshot(str(file_path.absolute()))
        else:
            raise ValueError('Capability not implemented for the driver type selected')

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

        with open(config.BOT_COOKIES_FILE, 'wb') as file:
            pickle.dump(cookies, file)
    
    def load_cookies(self):
        """
        Load Cookies

        Add all the cookies founded in the file.
        """
        if Path(config.BOT_COOKIES_FILE).is_file():
            with open(config.BOT_COOKIES_FILE, 'rb') as file:
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
    
    def __load_chrome_preferences__(self) -> dict:
        """
        Load Firefox Preferences

        Load all the preferences for chrome stored in a json file,
        specified in the config.
        """
        chrome_preferences: dict = {}

        if Path(config.BOT_PREFERENCES_FILE_PATH).exists():
            # load all the preferences in the file
            with open(config.BOT_PREFERENCES_FILE_PATH, 'r') as file:
                chrome_preferences = json.load(file)

        return chrome_preferences

    def __load_firefox_preferences__(self) -> FirefoxProfile:
        """
        Load Firefox Preferences

        Load all the preferences for firefox stored in a json file,
        specified in the config.
        """
        # initialize an empty profile for the settings
        firefox_profile: FirefoxProfile = FirefoxProfile()

        if Path(config.BOT_PREFERENCES_FILE_PATH).exists():
            # load all the preferences in the file
            with open(config.BOT_PREFERENCES_FILE_PATH, 'r') as file:
                data = json.load(file)

                # iterate all the data of the file
                for key, value in data.items():
                    firefox_profile.set_preference(key, value)

        return firefox_profile
    
    def __load_chrome_options__(self) -> ChromeOptions:
        """
        Load Chrome Options

        Load all the default chrome options
        """
        # chrome configurations
        chrome_options: ChromeOptions = ChromeOptions()
        # add all the arguments specified in the config
        for argument in config.BOT_ARGUMENTS:
            chrome_options.add_argument(argument)

        # basical static settings
        chrome_options.add_argument(f'user-agent={config.BOT_USER_AGENT}')

        chrome_preferences: dict = self.__load_chrome_preferences__()

        # basical static settings
        chrome_preferences['download.default_directory'] = self._temp_dir

        # add the preferences to the chrome options
        chrome_options.add_experimental_option("prefs", chrome_preferences)
        
        return chrome_options

    def __load_firefox_options__(self) -> FirefoxOptions:
        """
        Load Firefox Options

        Load all the default chrome options
        """
        # firefox configurations
        firefox_options: FirefoxOptions = FirefoxOptions()
        # add all the arguments specified in the config
        for argument in config.BOT_ARGUMENTS:
            firefox_options.add_argument(argument)

        firefox_profile: FirefoxProfile = self.__load_firefox_preferences__()

        # basical static settings, downlaod direcotry as the temp and user agent from config
        firefox_profile.set_preference('general.useragent.override', config.BOT_USER_AGENT)
        firefox_profile.set_preference('browser.download.folderList', 2)
        firefox_profile.set_preference('browser.download.dir', self._temp_dir)

        # add the profile to the firefox options
        firefox_options.profile = firefox_profile

        return firefox_options
    
    def __load_firefox_driver__(self) -> webdriver:
        """
        Load Firefox Driver

        Load and configure all the options for the firefox driver.
        """
        if config.BOT_PROXY_ENABLED:
            # proxy settings
            seleniumwire_options = {
                "proxy": {
                    "http": config.BOT_HTTP_PROXY,
                    "https": config.BOT_HTTPS_PROXY,
                }
            }

            # initialize firefox with proxy
            return Firefox(
                options=self.__load_firefox_options__(),
                seleniumwire_options=seleniumwire_options
            )
        
        # initialize firefox without proxy
        return Firefox(
            options=self.__load_firefox_options__()
        )

    def __load_chrome_driver__(self) -> webdriver:
        """
        Load Chrome Driver

        Load and configure all the options for the firefox driver.
        """
        if config.BOT_PROXY_ENABLED:
            # proxy settings
            seleniumwire_options = {
                "proxy": {
                    "http": config.BOT_HTTP_PROXY,
                    "https": config.BOT_HTTPS_PROXY,
                }
            }

            # initialize firefox with proxy
            return Chrome(
                options=self.__load_chrome_options__(),
                seleniumwire_options=seleniumwire_options
            )
        
        # initialize firefox without proxy
        return Chrome(
            options=self.__load_chrome_options__()
        )