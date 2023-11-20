import logging
from abc import ABC, abstractmethod
from typing import Type, Union, List

from selenium.webdriver.common.by import By

from fastbots.bot import Bot
from fastbots import config


logger = logging.getLogger(__name__)


class Page(ABC):
    """
    Page

    A web page blueprint used to forward pages and
    make a series of actions on it.
    """

    def __init__(self, bot: Bot, page_name: str = 'page_name'):
        """
        Initialize the page class.

        In the locators file must be declared the page in the below format:

        [pages_url]
        page_name=https://example.com/page
        """
        super().__init__()

        self._bot: Bot = bot
        self._page_name: str = page_name
        
        # load the pages url from the locators file
        self._page_url: str = self._bot.locator('pages_url', self._page_name)

        # check that the current page is the expected
        if config.SELENIUM_EXPECTED_URL_CHECK and self._page_url != 'None':
            self._bot.check_page_url(expected_page_url=self._page_url)

    @property
    def bot(self):
        return self._bot

    def __locator__(self, locator_name: str) -> tuple:
        """
        Locator

        Utility used to load the locator.

        The locators in the file must be in the below format:

        [page_name]
        locator_name=(By.XPATH, "//html//input")

        """
        # load the locators from file and interprete that as code
        full_locator: str = self._bot.locator(self._page_name, locator_name)

        if not full_locator.startswith('(') or not full_locator.endswith(')'):
            raise ValueError('The locator must be enclosed in round brackets.')

        # declared locators
        locator_list: List[str] = ['By.ID', 'By.XPATH', 'By.NAME', 'By.CLASS_NAME', 'By.CSS_SELECTOR', 
                                       'By.LINK_TEXT', 'By.PARTIAL_LINK_TEXT', 'By.TAG_NAME']

        # check the used locator
        parsed_locator: tuple = None
        for locator in locator_list:
            # check that the first characters are them of the locators and the next one of the comma 
            if full_locator[1:-1].strip().startswith(locator) and full_locator[1:-1].strip()[len(locator):].strip().startswith(','):
                # extract the tuple required as locator
                parsed_locator = (eval(locator), full_locator[1:-1].strip()[len(locator):].strip()[1:].strip()[1:-1])

                logging.info(f'{parsed_locator}')

                return parsed_locator
            
        else:
            raise ValueError('The specified locator is unknown or worng, check by, brackets and commas.')

    @abstractmethod
    def forward(self) -> Union[Type['Page'], None]:
        """
        Forward

        This method represents a series of action in one page,
        in order to pass on another page or when the task it's done
        it will return None, in order to finish.
        """
        raise NotImplementedError('Tasks must define this method.')