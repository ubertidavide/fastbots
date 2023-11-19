import logging

from fastbots import Task, Bot, Page, EC, WebElement, Keys


class ProductPage(Page):

    # page name it's the page_name used in the locators file, see below
    def __init__(self, bot: Bot, page_name: str = 'product_page'): 
        super().__init__(bot, page_name)

    def forward(self) -> None:
        logging.info('DO THINGS')

        # using the locators specified in the file give more flexibility and less code changes
        name_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('name_locator')))
        # store data in the payload section, useful when i need to retrieve data on success
        self.bot.payload['result'] = name_element.text

        # end the chain of pages interactins
        return None

class SearchPage(Page):

    # page name it's the page_name used in the locators file, see below
    def __init__(self, bot: Bot, page_name: str = 'search_page'):
        super().__init__(bot, page_name)

    def forward(self) -> ProductPage:
        logging.info('DO THINGS')

        # using the locators specified in the file give more flexibility and less code changes
        search_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('search_locator')))
        search_element.send_keys('Selenium with Python Simplified For Beginners')
        search_element.send_keys(Keys.ENTER)

        # product_element: WebElement = self.bot.driver.find_element(*self.__locator__('product_locator'))
        product_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('product_locator')))
        product_element.click()

        # continue the chain interaction in the next page
        return ProductPage(bot=self.bot)

class TestTask(Task):

    # main task code
    def run(self, bot: Bot) -> bool:
        logging.info('DO THINGS')

        # open the search page do things and go forward
        page: Page = SearchPage(bot=bot).forward()

        # for every page founded do things and go forward
        while page:
            page = page.forward()

        # for default it will succeed
        return True

    # method executed on bot success, with it's payload
    def on_success(self, payload):
        logging.info(f'SUCCESS {payload}')
    
    # method executed on bot failure
    def on_failure(self, payload):
        logging.info(f'FAILED {payload}')
        
if __name__ == '__main__':
    # start the above task
    TestTask()()