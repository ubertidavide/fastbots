import json
from pathlib import Path
from datetime import datetime
import logging

from seleniumwire.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver

from fastbots import config, Bot


logger = logging.getLogger(__name__)


class FirefoxBot(Bot):
    """
    Firefox Bot

    Class used to specify the Firefox Bot Implementation.
    """

    def __init__(self) -> None:
        """
        Bot

        Initialize all the attributes of the Firefox Bot instance
        """
        super().__init__()

        # load the onfigured driver
        self._driver: webdriver = self.__load_driver__()

        # default wait
        self._wait: WebDriverWait = WebDriverWait(driver=self._driver, timeout=config.SELENIUM_DEFAULT_WAIT, poll_frequency=1)

    
    def save_screenshot(self):
        """
        Save Screenshot

        Save the browser's screenshot to a png file, the path could be specified in the settings.
        """
        if not Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).exists():
            Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).mkdir(exist_ok=True, parents=True)

        file_path: Path = Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH) / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
        self._driver.get_full_page_screenshot_as_file(str(file_path.absolute()))

    def __load_preferences__(self) -> FirefoxProfile:
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

    def __load_options__(self) -> FirefoxOptions:
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
    
    def __load_driver__(self) -> webdriver:
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