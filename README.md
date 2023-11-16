# FastBOT
A simple library for bot development using selenium and the POM (Page Object Model) design.

```python
from typing import Type
from fastbot import Task, Bot, Page

import time
import logging


class SearchPage(Page):

    def __init__

    def forward(self) -> Type[Page] | None:
        logging.info('DO THINGS')
        # using the locators specified in the file give more flexibility and less code changes
        search_bar = self.bot.driver.find_element(*self.__locator__('search_locator'))
        logging.info(f'Searchbar: {search_bar.is_enabled}')
        return None

class ProductPage(Page):

    def forward(self) -> Type[Page] | None:
        logging.info('DO THINGS')
        # using the locators specified in the file give more flexibility and less code changes
        search_bar = self.bot.driver.find_element(*self.__locator__('search_locator'))
        logging.info(f'Searchbar: {search_bar.is_enabled}')
        return None

class TestTask(Task):

    # retried n times
    def run(self, bot: Bot) -> bool:
        logging.info('DO THINGS')
        SearchPage(bot, page_name='amazon_page').forward()
        return True

    # success part
    def on_success(self):
        logging.info('SUCCESS')
    
    # failure part
    def on_failure(self, retry_state):
        logging.info('FAILED')
        
if __name__ == '__main__':
    # start the task
    TestTask()()
```

## TODO:
1. Adding more documentation and stabilize the code
2. Add a cookiecutter example