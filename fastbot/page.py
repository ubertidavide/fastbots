import logging
from abc import ABC, abstractmethod
from typing import Type, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from fastbot.bot import Bot


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
        self.bot: Bot = bot
        self.page_name: str = page_name
        super().__init__()
        
        # load the pages url from the locators file
        self.page_url: str = self.bot.locator('pages_url', self.page_name)

        # check that the current page is the expected
        if self.page_url != 'None':
            self.bot.check_page_url(expected_page_url=self.page_url)

    def __locator__(self, locator_name: str) -> tuple:
        """
        Locator

        Utility used to load the locator.

        The locators in the file must be in the below format:

        [page_name]
        locator_name=(By.XPATH, "//html//input")

        """
        # load the locators from file and interprete that as code
        return eval(self.bot.locator(self.page_name, locator_name))

    @abstractmethod
    def forward(self) -> Union[Type['Page'], None]:
        """
        Forward

        This method represents a series of action in one page,
        in order to pass on another page or when the task it's done
        it will return None, in order to finish.
        """
        raise NotImplementedError('Tasks must define this method.')