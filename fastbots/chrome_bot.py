import json
from pathlib import Path
import logging

from seleniumwire.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver

from fastbots import config, Bot


logger = logging.getLogger(__name__)


class ChromeBot(Bot):
    """
    Chrome Bot

    Class used to specify a bot blueprint.
    """

    def __init__(self) -> None:
        """
        Chrome Bot

        Initialize all the attributes of the Chrome Bot instance
        """
        super().__init__()

        # load the onfigured driver
        self._driver: webdriver = self.__load_driver__()

        # default wait
        self._wait: WebDriverWait = WebDriverWait(driver=self._driver, timeout=config.SELENIUM_DEFAULT_WAIT, poll_frequency=1)
    
    def __load_preferences__(self) -> dict:
        """
        Load Chrome Preferences

        Load all the preferences for chrome stored in a json file,
        specified in the config.
        """
        chrome_preferences: dict = {}

        if Path(config.BOT_PREFERENCES_FILE_PATH).exists():
            # load all the preferences in the file
            with open(config.BOT_PREFERENCES_FILE_PATH, 'r') as file:
                chrome_preferences = json.load(file)

        return chrome_preferences
    
    def __load_options__(self) -> ChromeOptions:
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

    def __load_driver__(self) -> webdriver:
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