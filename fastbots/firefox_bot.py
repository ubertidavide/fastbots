import json
from pathlib import Path
from datetime import datetime
import logging

from seleniumwire.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from fastbots import config, Bot


logger = logging.getLogger(__name__)

class FirefoxBot(Bot):
    """
    Firefox Bot

    Class representing the Firefox Bot implementation.

    Attributes:
        _driver (WebDriver): The WebDriver instance for Firefox.
        _wait (WebDriverWait): The WebDriverWait instance for Firefox.

    Methods:
        __init__(): Initializes all attributes of the Firefox Bot instance.
        save_screenshot(): Saves the browser's screenshot to a PNG file.
        __load_preferences__(): Loads Firefox preferences from a JSON file.
        __load_options__(): Loads Firefox options, including user agent and download directory.
        __load_driver__(): Loads and configures options for the Firefox driver.

    Example:
        ```python
        with FirefoxBot() as bot:
            bot.save_screenshot()
        ```
    """

    def __init__(self) -> None:
        """
        Initializes all attributes of the Firefox Bot instance.
        """
        super().__init__()

        # Load the configured driver
        self._driver: WebDriver = self.__load_driver__()

        # Default wait
        self._wait: WebDriverWait = WebDriverWait(driver=self._driver, timeout=config.SELENIUM_DEFAULT_WAIT, poll_frequency=1)

    def save_screenshot(self):
        """
        Saves the browser's screenshot to a PNG file.

        The file path can be specified in the settings.
        """
        if not Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).exists():
            Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).mkdir(exist_ok=True, parents=True)

        file_path: Path = Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH) / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
        self._driver.get_full_page_screenshot_as_file(str(file_path.absolute()))

    def __load_preferences__(self) -> FirefoxProfile:
        """
        Load Firefox Preferences

        Load all the preferences for Firefox stored in a JSON file, specified in the config.

        Returns:
            FirefoxProfile: The Firefox profile with loaded preferences.
        """
        # Initialize an empty profile for the settings
        firefox_profile: FirefoxProfile = FirefoxProfile()

        if Path(config.BOT_PREFERENCES_FILE_PATH).exists():
            # Load all the preferences from the file
            with open(config.BOT_PREFERENCES_FILE_PATH, 'r') as file:
                data = json.load(file)

                # Iterate through all the data in the file
                for key, value in data.items():
                    firefox_profile.set_preference(key, value)

        return firefox_profile

    def __load_options__(self) -> FirefoxOptions:
        """
        Load Firefox Options

        Load all the default Firefox options.

        Returns:
            FirefoxOptions: The configured Firefox options.
        """
        # Firefox configurations
        firefox_options: FirefoxOptions = FirefoxOptions()
        
        # Add all the arguments specified in the config
        for argument in config.BOT_ARGUMENTS:
            firefox_options.add_argument(argument)

        firefox_profile: FirefoxProfile = self.__load_preferences__()

        # Basic static settings: download directory as temp and user agent from config
        firefox_profile.set_preference('general.useragent.override', config.BOT_USER_AGENT)
        firefox_profile.set_preference('browser.download.folderList', 2)
        firefox_profile.set_preference('browser.download.dir', self._temp_dir)

        # Add the profile to the Firefox options
        firefox_options.profile = firefox_profile

        return firefox_options
    
    def __load_driver__(self) -> WebDriver:
        """
        Load Firefox Driver

        Load and configure all the options for the Firefox driver.

        Returns:
            WebDriver: The configured WebDriver instance for Firefox.
        """
        if config.BOT_PROXY_ENABLED:
            # Proxy settings
            seleniumwire_options = {
                "proxy": {
                    "http": config.BOT_HTTP_PROXY,
                    "https": config.BOT_HTTPS_PROXY,
                }
            }

            # Initialize Firefox with proxy
            return Firefox(
                options=self.__load_options__(),
                seleniumwire_options=seleniumwire_options
            )
        
        # Initialize Firefox without proxy
        return Firefox(
            options=self.__load_options__()
        )
