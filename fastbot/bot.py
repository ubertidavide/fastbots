import tempfile
import json
import shutil
import pickle
from typing import List
from pathlib import Path
import datetime
import configparser
import logging

from seleniumwire.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from fastbot import config, logger
from fastbot.exceptions import ExpectedUrlError


logger = logging.getLogger(__name__)


class Bot(object):
    """
    Bot

    Class used to specify an implementation of a bot,
    with all it's related basics stuff.
    """
        
    def __enter__(self):
        """
        Enter

        Load and configure all the needed resources.
        """
        # data used from pages 
        self.payload: dict = {}

        # use a temporary directory as default download folder
        if config.BOT_DOWNLOAD_FOLDER_PATH != 'None':
            self.temp_dir: str = tempfile.mkdtemp(dir=config.BOT_DOWNLOAD_FOLDER_PATH)
        else:
            self.temp_dir: str = tempfile.mkdtemp()

        # firefox configurations
        firefox_options: Options = Options()
        # add all the arguments specified in the config
        for argument in config.FIREFOX_ARGUMENTS:
            firefox_options.add_argument(argument.strip())

        firefox_profile: FirefoxProfile = self.__load_preferences__()

        # basical static settings, downlaod direcotry as the temp and user agent from config
        firefox_profile.set_preference('general.useragent.override', config.FIREFOX_USER_AGENT)
        firefox_profile.set_preference('browser.download.folderList', 2)
        firefox_profile.set_preference('browser.download.dir', self.temp_dir)

        # add the profile to the firefox options
        firefox_options.profile = firefox_profile

        if config.FIREFOX_PROXY_ENABLED:

            proxies = {
                "proxy": {
                    "http": config.FIREFOX_HTTP_PROXY,
                    "https": config.FIREFOX_HTTPS_PROXY,
                }
            }

            # initialize firefox with proxy
            self.driver: Firefox = Firefox(
                options=firefox_options,
                seleniumwire_options=proxies
            )
        else:
            # initialize firefox without proxy
            self.driver: Firefox = Firefox(
                options=firefox_options
            )

        # default global driver settings
        self.locators = self.__load_locators__()
        self.driver.implicitly_wait(config.SELENIUM_GLOBAL_IMPLICIT_WAIT)

        # default wait
        self.wait: WebDriverWait = WebDriverWait(driver=self.driver, timeout=config.SELENIUM_DEFAULT_WAIT, poll_frequency=1)

        # load the start page
        self.driver.get(self.locator('pages_url', 'start_url'))

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Exit
        
        Clean all the used resources.
        """
        shutil.rmtree(self.temp_dir)
        self.driver.close()

    def check_page_url(self, expected_page_url: str):
        """
        Check Page Url

        Check that the browser it't at the expected page.
        """
        try:
            # polling that the page url is the expected
            WebDriverWait(driver=self.driver, timeout=config.SELENIUM_EXPECTED_URL_TIMEOUT, poll_frequency=1).until(
                EC.url_to_be(expected_page_url)
            )

        except TimeoutException as te:
            # if not the expected url raises an exception
            raise ExpectedUrlError(current_url=self.driver.current_url, expected_url=expected_page_url)

    def locator(self, page_name: str, locator_name: str):
        """
        Locator

        Getter that get the locator used for a page locator
        """
        return self.locators.get(page_name, locator_name)

    def __load_locators__(self) -> configparser:
        """
        Load Locators

        Load a file that contains all the locators
        """
        config_parser: configparser = configparser.ConfigParser()
        config_parser.read(config.SELENIUM_LOCATORS_FILE)
        return config_parser

    def __load_preferences__(self) -> FirefoxProfile:
        """
        Load Preferences

        Load all the preferences stored in a json file,
        specified in the config.
        """
        # initialize an empty profile for the settings
        firefox_profile: FirefoxProfile = FirefoxProfile()

        if Path(config.FIREFOX_PREFERENCES_FILE_PATH).exists():
            # load all the preferences in the file
            with open(config.FIREFOX_PREFERENCES_FILE_PATH, 'r') as file:
                data = json.load(file)

                # iterate all the data of the file
                for key, value in data.items():
                    firefox_profile.set_preference(key, value)

        return firefox_profile

    def save_screenshot(self):
        """
        Save Screenshot

        Save the browser's screenshot to a png file, the path could be specified in the settings.
        """
        if not Path(config.FIREFOX_SCREENSHOT_DOWNLOAD_FOLDER_PATH).exists():
            Path(config.FIREFOX_SCREENSHOT_DOWNLOAD_FOLDER_PATH).mkdir(exist_ok=True, parents=True)

        file_path: Path = Path(config.FIREFOX_SCREENSHOT_DOWNLOAD_FOLDER_PATH) / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
        self.driver.get_full_page_screenshot_as_file(str(file_path.absolute()))

    def save_html(self):
        """
        Save Html

        Save the browser's html page to a file, the path could be specified in the settings.
        """
        if not Path(config.FIREFOX_HTML_DOWNLOAD_FOLDER_PATH).exists():
            Path(config.FIREFOX_HTML_DOWNLOAD_FOLDER_PATH).mkdir(exist_ok=True, parents=True)

        file_path: Path = Path(config.FIREFOX_HTML_DOWNLOAD_FOLDER_PATH) / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.html'
        with open(str(file_path.absolute()), "w", encoding="utf-8") as file:
            file.write(self.driver.page_source)

    def save_cookies(self):
        """
        Save Cookies

        Save all the cookies founded in the file.
        """
        cookies: List[dict] = self.driver.get_cookies()

        with open(config.FIREFOX_COOKIES_FILE, 'wb') as file:
            pickle.dump(cookies, file)
    
    def load_cookies(self):
        """
        Load Cookies

        Add all the cookies founded in the file.
        """
        with open(config.FIREFOX_COOKIES_FILE, 'rb') as file:
            cookies = pickle.load(file)

            for cookie in cookies:
                self.driver.add_cookie(cookie)
