import tempfile
import shutil
import pickle
from typing import List, Union
from pathlib import Path
from datetime import datetime
from configparser import ConfigParser
import logging
from typing import Type
from abc import ABC, abstractmethod

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver

from fastbots import config, logger
from fastbots.exceptions import ExpectedUrlError, DownloadFileError


logger = logging.getLogger(__name__)


class Bot(ABC):
    """
    Base class for creating web automation bots using Selenium.

    Attributes:
        _temp_dir (str): A temporary directory for storing files during the bot's operation.
        _download_dir (str): The directory where downloaded files are stored.
        _locators (ConfigParser): Configuration parser for managing locators.
        _payload (dict): Data store for the bot.

    Methods:
        __init__(): Initializes the Bot instance.
        __enter__(): Enters a context and loads/configures resources.
        __exit__(): Exits a context and cleans up resources.
        check_page_url(expected_page_url: str): Checks if the browser is on the expected page URL.
        locator(page_name: str, locator_name: str) -> str: Retrieves a locator for a given page.
        wait_downloaded_file_path(file_extension: str, new_file_name: str | None = None) -> str:
            Waits for a specific downloaded file and returns its path.
        save_screenshot(): Saves a screenshot of the browser.
        save_html(): Saves the HTML page of the browser.
        save_cookies(): Saves all the cookies found in the browser.
        load_cookies(): Loads and adds cookies from a file.
        __load_locators__() -> ConfigParser: Loads locators from a configuration file.
        __load_preferences__() -> Union[FirefoxProfile, dict]:
            Loads preferences stored in a JSON file specified in the configuration.
        __load_options__() -> Union[FirefoxOptions, ChromeOptions]: Loads default options.
        __load_driver__() -> WebDriver: Loads and configures the driver.
    """

    def __init__(self) -> None:
        """
        Initializes the Bot instance.

        Sets up temporary directories, locators, and a data store for the bot.
        """
        super().__init__()

        # use a temporary directory as default download folder
        self._temp_dir: str = tempfile.mkdtemp()

        # official downloaded file folder
        if config.BOT_DOWNLOAD_FOLDER_PATH != 'None':
            self._download_dir: str = tempfile.mkdtemp(dir=config.BOT_DOWNLOAD_FOLDER_PATH)
        else:
            self._download_dir: str = tempfile.mkdtemp()

        # load all the locators
        self._locators: ConfigParser = self.__load_locators__()
        # data store
        self._payload: dict = {}

    @property
    def driver(self) -> WebDriver:
        """
        Gets the Selenium WebDriver instance used by the bot.

        Returns:
            WebDriver: The Selenium WebDriver instance.
        """
        return self._driver
    
    @property
    def wait(self) -> WebDriverWait:
        """
        Gets the WebDriverWait instance used for waiting in the bot.

        Returns:
            WebDriverWait: The WebDriverWait instance.
        """
        return self._wait
    
    @property
    def payload(self) -> dict:
        """
        Gets the payload dictionary used to store data in the bot.

        Returns:
            dict: The payload dictionary.
        """
        return self._payload

    def __enter__(self) -> Type['Bot']:
        """
        Enters a context and loads/configures resources.

        Sets up implicit wait and navigates to the start URL.

        Returns:
            Type['Bot']: The bot instance within the context.
        """
        # default global driver settings
        self._driver.implicitly_wait(config.SELENIUM_GLOBAL_IMPLICIT_WAIT)

        # load the start page
        self._driver.get(self.locator('pages_url', 'start_url'))

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Exits a context and cleans up resources.

        Removes temporary directories and closes the driver.
        """
        shutil.rmtree(self._temp_dir)
        self._driver.close()

    def check_page_url(self, expected_page_url: str):
        """
        Checks if the browser is on the expected page URL.

        Args:
            expected_page_url (str): The expected page URL.

        Raises:
            ExpectedUrlError: If the browser is not on the expected page URL.
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
        Retrieves a locator for a given page.

        Args:
            page_name (str): The name of the page.
            locator_name (str): The name of the locator.

        Returns:
            str: The locator string.

        Raises:
            ValueError: If the specified page_name or locator_name is not declared in locators config.
        """
        if not self._locators.has_section(page_name):
            raise ValueError(f'The specified page_name: {page_name} is not declared in locators config.')
        
        if not self._locators.has_option(page_name, locator_name):
            raise ValueError(f'The specified locator_name: {locator_name} is not declared in locators config.')
        
        return self._locators.get(page_name, locator_name)
        
    def wait_downloaded_file_path(self, file_extension: str, new_file_name: str | None = None) -> str:
        """
        Waits for a specific downloaded file and returns its path.

        Args:
            file_extension (str): The file extension without the dot (e.g., "png" instead of ".png").
            new_file_name (str | None): The new file name if renaming is needed.

        Returns:
            str: The path of the downloaded file.

        Raises:
            DownloadFileError: If an error occurs during the file download.
        """
        try:
            # polling that the page url is the expected, it uses the extension because the temp part file cache by browser
            # usally have a specific extension that isn't the usally of the files
            WebDriverWait(driver=self._driver, timeout=config.SELENIUM_FILE_DOWNLOAD_TIMEOUT, poll_frequency=1).until(
                lambda driver: len(list(Path(self._temp_dir).glob(f'*.{file_extension}'))) == 1
            )

            # get the latest downloaded file
            latest_file: Path = max(list(Path(self._temp_dir).glob(f'*.{file_extension}')), key=lambda x: x.stat().st_ctime)

            # build the download path based on renamed file or 
            downloaded_file_path: Path = None
            if new_file_name is None:
                downloaded_file_path = Path(config.BOT_DOWNLOAD_FOLDER_PATH) / latest_file.name
            else:
                downloaded_file_path = Path(config.BOT_DOWNLOAD_FOLDER_PATH) / f'{new_file_name}.{file_extension}'
                
            # move to the download folder the file name
            shutil.move(src=str(latest_file.absolute()), dst=str(downloaded_file_path.absolute()))

            # remove the temporary downloaded file
            latest_file.unlink()

            # return the path and filename as string
            return str(downloaded_file_path.absolute())

        except TimeoutException as te:
            # if not the expected url raises an exception
            file_count: int = len(list(Path(self._temp_dir).glob(f'*.{file_extension}')))

            # error string based on the specific error
            if file_count == 0:
                raise DownloadFileError('File not founded in the download folder, an error with the download occurs.')
            elif file_count > 1:
                raise DownloadFileError(f'Too many downloaded files founded, files number : {file_count}.')

            raise DownloadFileError()

    def save_screenshot(self):
        """
        Saves a screenshot of the browser.

        Example:
        ```python
        bot = MyBot()
        bot.save_screenshot()
        ```
        """
        if not Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).exists():
            Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).mkdir(exist_ok=True, parents=True)

        file_path: Path = Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH) / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
        self._driver.save_screenshot(str(file_path.absolute()))

    def save_html(self):
        """
        Saves the HTML page of the browser.

        Example:
        ```python
        bot = MyBot()
        bot.save_html()
        ```
        """
        if not Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH).exists():
            Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH).mkdir(exist_ok=True, parents=True)

        file_path: Path = Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH) / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.html'
        with open(str(file_path.absolute()), "w", encoding="utf-8") as file:
            file.write(self._driver.page_source)

    def save_cookies(self):
        """
        Saves all the cookies found in the browser.

        Example:
        ```python
        bot = MyBot()
        bot.save_cookies()
        ```
        """
        cookies: List[dict] = self._driver.get_cookies()

        with open(config.BOT_COOKIES_FILE_PATH, 'wb') as file:
            pickle.dump(cookies, file)
    
    def load_cookies(self):
        """
        Loads and adds cookies from a file to the browser.

        Example:
        ```python
        bot = MyBot()
        bot.load_cookies()
        ```
        """
        if Path(config.BOT_COOKIES_FILE_PATH).is_file():
            with open(config.BOT_COOKIES_FILE_PATH, 'rb') as file:
                cookies = pickle.load(file)

                for cookie in cookies:
                    self._driver.add_cookie(cookie)

    def __load_locators__(self) -> ConfigParser:
        """
        Loads locators from a configuration file.

        Returns:
            ConfigParser: An instance of ConfigParser with loaded locators.

        Example:
        ```python
        bot = MyBot()
        locators = bot.__load_locators__()
        ```
        """
        if not Path(config.SELENIUM_LOCATORS_FILE).is_file():
            return ValueError(f'Erorr, locators file not founded at path: {config.SELENIUM_LOCATORS_FILE}')
        
        config_parser: ConfigParser = ConfigParser()
        config_parser.read(config.SELENIUM_LOCATORS_FILE)
        return config_parser

    @abstractmethod
    def __load_preferences__(self) -> Union[FirefoxProfile, dict]:
        """
        Loads preferences stored in a JSON file specified in the configuration.

        Returns:
            Union[FirefoxProfile, dict]: Either a FirefoxProfile or a dictionary of preferences.

        Example:
        ```python
        class MyBot(Bot):
            def __load_preferences__(self):
                # your implementation here
        ```
        """
        return NotImplementedError('Bot must define this method.')

    @abstractmethod
    def __load_options__(self) -> Union[FirefoxOptions, ChromeOptions]:
        """
        Loads default options.

        Returns:
            Union[FirefoxOptions, ChromeOptions]: Either FirefoxOptions or ChromeOptions.

        Example:
        ```python
        class MyBot(Bot):
            def __load_options__(self):
                # your implementation here
        ```
        """
        return NotImplementedError('Bot must define this method.')
    
    @abstractmethod
    def __load_driver__(self) -> WebDriver:
        """
        Loads and configures the driver.

        Returns:
            WebDriver: An instance of Selenium WebDriver.

        Example:
        ```python
        class MyBot(Bot):
            def __load_driver__(self):
                # your implementation here
        ```
        """
        return NotImplementedError('Bot must define this method.')
