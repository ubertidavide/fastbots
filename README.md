# FastBOT
A simple library for bot development using selenium and the POM (Page Object Model) design.

## Showcase:
Simple example, i will create a cookiecutter example.
```python
import logging

from selenium.webdriver.support import expected_conditions as EC

from fastbot import Task, Bot, Page


class ProductPage(Page):

    def __init__(self, bot: Bot, page_name: str = 'product_page'):
        super().__init__(bot, page_name)

    def forward(self) -> None:
        logging.info('DO THINGS')

        # using the locators specified in the file give more flexibility and less code changes
        name_element = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('name_locator')))
        # store data in the payload section, useful when i need to retrieve data on success
        self.bot.payload['result'] = name_element.text

        return None

class SearchPage(Page):

    def __init__(self, bot: Bot, page_name: str = 'search_page'):
        super().__init__(bot, page_name)

    def forward(self) -> ProductPage:
        logging.info('DO THINGS')

        # using the locators specified in the file give more flexibility and less code changes
        search_element = self.bot.driver.find_element(*self.__locator__('search_locator'))
        search_element.send_keys('product name\n')

        product_element = self.bot.driver.find_element(*self.__locator__('product_locator'))
        product_element.click()

        return ProductPage(bot=self.bot)

class TestTask(Task):

    # retried n times
    def run(self, bot: Bot) -> bool:
        logging.info('DO THINGS')

        page: Page = SearchPage(bot).forward()

        while page:
            page = page.forward()

        return True

    # success part
    def on_success(self, payload):
        logging.info(f'SUCCESS {payload["result"]}')
    
    # failure part
    def on_failure(self, payload):
        logging.info(f'FAILED {payload["result"]}')
        
if __name__ == '__main__':
    # start the task
    TestTask()()
```

## TODO:
1. Adding more documentation and stabilize the code
2. Add a cookiecutter example