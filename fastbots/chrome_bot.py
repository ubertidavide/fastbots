import json
from pathlib import Path
import logging

from seleniumwire.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from fastbots import config, Bot


logger = logging.getLogger(__name__)


class ChromeBot(Bot):
    """
    Chrome Bot

    Class used to specify a bot blueprint.

    Attributes:
        _driver (WebDriver): The Selenium WebDriver instance for Chrome.
        _wait (WebDriverWait): The default WebDriverWait instance for Chrome.

    Methods:
        __init__(): Initializes the ChromeBot instance.
        __load_preferences__(): Load Chrome preferences from a JSON file.
        __load_options__(): Load default Chrome options.
        __load_driver__(): Load and configure the Chrome WebDriver.

    Example:
        ```python
        try:
            # Create an instance of ChromeBot
            chrome_bot = ChromeBot()
            # Perform actions using the bot
            # ...
        finally:
            # Close the bot to release resources
            chrome_bot.close()
        ```
    """

    def __init__(self) -> None:
        """
        Chrome Bot

        Initialize all the attributes of the Chrome Bot instance.
        """
        super().__init__()

        # Load the configured driver
        self._driver: WebDriver = self.__load_driver__()

        # Default wait
        self._wait: WebDriverWait = WebDriverWait(driver=self._driver, timeout=config.SELENIUM_DEFAULT_WAIT,
                                                   poll_frequency=1)
    
    def __load_preferences__(self) -> dict:
        """
        Load Chrome Preferences

        Load all the preferences for Chrome stored in a JSON file, specified in the config.

        Returns:
            dict: Dictionary containing Chrome preferences.
        """
        chrome_preferences: dict = {}

        if Path(config.BOT_PREFERENCES_FILE_PATH).exists():
            # Load all the preferences from the file
            with open(config.BOT_PREFERENCES_FILE_PATH, 'r') as file:
                chrome_preferences = json.load(file)

        return chrome_preferences
    
    def __load_options__(self) -> ChromeOptions:
        """
        Load Chrome Options

        Load all the default Chrome options.

        Returns:
            ChromeOptions: ChromeOptions instance with configured options.
        """
        # Chrome configurations
        chrome_options: ChromeOptions = ChromeOptions()
        
        # Add all the arguments specified in the config
        for argument in config.BOT_ARGUMENTS:
            chrome_options.add_argument(argument)

        # Basic static settings
        chrome_options.add_argument(f'user-agent={config.BOT_USER_AGENT}')

        # Load preferences
        chrome_preferences: dict = self.__load_preferences__()

        # Basic static settings
        chrome_preferences['download.default_directory'] = self._temp_dir

        # Add preferences to Chrome options
        chrome_options.add_experimental_option("prefs", chrome_preferences)
        
        return chrome_options

    def __load_driver__(self) -> WebDriver:
        """
        Load Chrome Driver

        Load and configure all the options for the Chrome driver.

        Returns:
            WebDriver: Chrome WebDriver instance.
        """
        if config.BOT_PROXY_ENABLED:
            # Proxy settings
            seleniumwire_options = {
                "proxy": {
                    "http": config.BOT_HTTP_PROXY,
                    "https": config.BOT_HTTPS_PROXY,
                }
            }

            # Initialize Chrome with proxy
            return Chrome(
                options=self.__load_options__(),
                seleniumwire_options=seleniumwire_options
            )
        
        # Initialize Chrome without proxy
        return Chrome(
            options=self.__load_options__()
        )
