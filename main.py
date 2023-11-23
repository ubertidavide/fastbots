-- main.py
# Import the logging module to handle logging in the script
import logging

# Import necessary classes and modules from the fastbots library
from fastbots import Task, Bot, Page, EC, WebElement, Keys

# Define a ProductPage class, which is a subclass of the Page class
class ProductPage(Page):

    # Constructor to initialize the ProductPage instance
    # The page_name is used in the locators file; default is 'product_page'
    def __init__(self, bot: Bot, page_name: str = 'product_page'): 
        super().__init__(bot, page_name)

    # Define the forward method for navigating to the next page
    def forward(self) -> None:
        # Log information about the current action
        logging.info('DO THINGS')

        # Use locators specified in the file for flexibility and less code changes
        name_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('name_locator')))
        
        # Store data in the payload section for future retrieval on success
        self.bot.payload['result'] = name_element.text

        # End the chain of page interactions
        return None

# Define a SearchPage class, which is a subclass of the Page class
class SearchPage(Page):

    # Constructor to initialize the SearchPage instance
    # The page_name is used in the locators file; default is 'search_page'
    def __init__(self, bot: Bot, page_name: str = 'search_page'):
        super().__init__(bot, page_name)

    # Define the forward method for navigating to the next page (ProductPage)
    def forward(self) -> ProductPage:
        # Log information about the current action
        logging.info('DO THINGS')

        # Use locators specified in the file for flexibility and less code changes
        search_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('search_locator')))
        
        # Enter a search query and submit
        search_element.send_keys('Selenium with Python Simplified For Beginners')
        search_element.send_keys(Keys.ENTER)

        # Locate the product element and click on it
        product_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('product_locator')))
        product_element.click()

        # Continue the chain of interaction on the next page (ProductPage)
        return ProductPage(bot=self.bot)

# Define a TestTask class, which is a subclass of the Task class
class TestTask(Task):

    # Main task code to be executed when running the script
    def run(self, bot: Bot) -> bool:
        # Log information about the current action
        logging.info('DO THINGS')

        # Open the search page, perform actions, and go forward
        page: Page = SearchPage(bot=bot).forward()

        # For every page found, perform actions and go forward
        while page:
            page = page.forward()

        # For default, the task will succeed
        return True

    # Method executed on bot success, with its payload
    def on_success(self, payload):
        logging.info(f'SUCCESS {payload}')
    
    # Method executed on bot failure
    def on_failure(self, payload):
        logging.info(f'FAILED {payload}')

# Check if the script is executed as the main program
if __name__ == '__main__':
    # Start the above TestTask
    TestTask()()
