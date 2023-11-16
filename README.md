# FastBOT
A simple library for bot development using selenium and the POM (Page Object Model) design.

## Installation:
The installation is a simple process with pip on the
PyPy repository.
```bash
pip install fastbot
```

## Showcase:
Simple example, i will create a cookiecutter example.
```python
import logging

from fastbot import Task, Bot, Page, EC, WebElement


class ProductPage(Page):

    def __init__(self, bot: Bot, page_name: str = 'product_page'):
        super().__init__(bot, page_name)

    def forward(self) -> None:
        logging.info('DO THINGS')

        # using the locators specified in the file give more flexibility and less code changes
        name_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('name_locator')))
        # store data in the payload section, useful when i need to retrieve data on success
        self.bot.payload['result'] = name_element.text

        return None

class SearchPage(Page):

    def __init__(self, bot: Bot, page_name: str = 'search_page'):
        super().__init__(bot, page_name)

    def forward(self) -> ProductPage:
        logging.info('DO THINGS')

        # using the locators specified in the file give more flexibility and less code changes
        search_element: WebElement = self.bot.driver.find_element(*self.__locator__('search_locator'))
        search_element.send_keys('product name\n')

        product_element: WebElement = self.bot.driver.find_element(*self.__locator__('product_locator'))
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

And in the locators configuration file there is all the required config.
This could be change easily without rebuild or make modifications at the code.
```ini
[pages_url]
start_url=https://www.amazon.com/
search_page=https://www.amazon.com/
product_page=https://www.amazon.com/Volunteer-Lanyards-Identification-Volunteers-Hospital/dp/B0CL4QC72R/ref=sr_1_1_sspa?crid=1QXA5N1RYJFQX&keywords=product+name&qid=1700128009&sprefix=product+name%2Caps%2C165&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1

[search_page]
search_locator=(By.ID, "twotabsearchtextbox")
product_locator=(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]')

[product_page]
name_locator=(By.ID, "title")
```

## TODO:
1. Adding more documentation and stabilize the code
2. Add a cookiecutter example