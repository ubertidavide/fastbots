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

    A blueprint for web pages used to navigate and perform actions on them.

    Attributes:
        _bot (Bot): The bot instance associated with the page.
        _page_name (str): The name of the page.
        _page_url (str): The URL of the page.

    Methods:
        __init__(bot: Bot, page_name: str = 'page_name'): Initializes the Page class.
        bot: Gets the associated bot instance.
        __locator__(locator_name: str) -> tuple: Utility method to load a locator.
        forward() -> Union[Type['Page'], None]: Represents a series of actions on the page.

    Example:
        ```python
        class MyPage(Page):
            def forward(self):
                # your implementation here
        ```
    """

    def __init__(self, bot: Bot, page_name: str = 'page_name', strict_page_check: bool = True):
        """
        Initializes the Page class.

        In the locators file, the page must be declared in the format:
        [pages_url]
        page_name=https://example.com/page

        Args:
            bot (Bot): The bot instance associated with the page.
            page_name (str): The name of the page.
            strict_page_check (bool): True -> Check if the page url it's the same of the current url, 
                                    else False -> if the url contain the page url.

        Raises:
            ValueError: If the locator is not enclosed in round brackets.
        """
        super().__init__()

        self._bot: Bot = bot
        self._page_name: str = page_name
        
        # load the pages url from the locators file
        self._page_url: str = self._bot.locator('pages_url', self._page_name)

        # check that the current page is the expected
        if config.SELENIUM_EXPECTED_URL_CHECK and self._page_url != 'None':
            self._bot.check_page_url(expected_page_url=self._page_url, strict_page_check=strict_page_check)

    @property
    def bot(self):
        """
        Gets the associated bot instance.

        Returns:
            Bot: The bot instance.
        """
        return self._bot

    def __locator__(self, locator_name: str) -> tuple:
        """
        Utility method to load a locator.

        The locators in the file must be in the format:
        [page_name]
        locator_name=(By.XPATH, "//html//input")

        Args:
            locator_name (str): The name of the locator.

        Returns:
            tuple: A tuple representing the loaded locator.

        Raises:
            ValueError: If the locator is not enclosed in round brackets or is of an unknown or incorrect format.
        """
        # load the locators from file and interpret that as code
        full_locator: str = self._bot.locator(self._page_name, locator_name).strip().replace('\\\'',  '\'').replace('\\"', '"')

        if not full_locator.startswith('(') or not full_locator.endswith(')'):
            raise ValueError('The locator must be enclosed in round brackets.')

        # declared locators
        locator_list: List[str] = [
            'By.ID', 'By.XPATH', 'By.NAME', 'By.CLASS_NAME', 'By.CSS_SELECTOR', 
            'By.LINK_TEXT', 'By.PARTIAL_LINK_TEXT', 'By.TAG_NAME'
        ]

        # check the used locator
        parsed_locator: tuple = None
        for locator in locator_list:
            # check that the first characters are them of the locators and the next one of the comma 
            if full_locator[1:-1].strip().startswith(locator) and full_locator[1:-1].strip()[len(locator):].strip().startswith(','):
                # extract the tuple required as locator
                parsed_locator = (
                    eval(locator), 
                    full_locator[1:-1].strip()[len(locator):].strip()[1:].strip()[1:-1]
                )

                logging.debug(f'{locator_name} {parsed_locator}')

                return parsed_locator
            
        else:
            raise ValueError('The specified locator is unknown or wrong; check by, brackets, and commas.')

    @abstractmethod
    def forward(self) -> Union[Type['Page'], None]:
        """
        Represents a series of actions on the page.

        Returns:
            Union[Type['Page'], None]: Either the next page instance or None to finish.

        Raises:
            NotImplementedError: Subclasses must define this method.
        """
        raise NotImplementedError('Tasks must define this method.')
