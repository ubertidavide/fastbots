# Import the logging module to handle logging in the script
import logging

# Import necessary classes and modules from the fastbots library
from fastbots import Task, Bot, Page, Payload, EC, WebElement, Keys, ActionChains, Select, Alert, TimeoutException, NoSuchElementException

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
        # name_element: WebElement = self.bot.driver.find_element(*self.__locator__('name_locator'))
        #name_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('name_locator')))
        
        # Store data in the payload section for future retrieval on success
        #self.bot.payload.input_data['element_name'] = name_element.text

        # example of downloading the product png images and rename it (check download folder settings)
        # name_element.click() for example on element download button
        # self.bot.wait_downloaded_file_path("png", new_name_file=self.bot.payload.input_data['element_name'])
        # it will put the download path in the payload.downloads datastore class when downloaded and renamed

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
        
        # Enter a search query and submit (using the loaded data in the task)
        search_element.send_keys(self.bot.payload.input_data['element_name'])
        search_element.send_keys(Keys.ENTER)

        # Locate the product element and click on it
        #product_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('product_locator')))
        #product_element.click()

        # Continue the chain of interaction on the next page (ProductPage)
        return ProductPage(bot=self.bot)

# Define a TestTask class, which is a subclass of the Task class
class TestTask(Task):

    # Main task code to be executed when running the script
    def run(self, bot: Bot) -> bool:
        # Log information about the current action
        logging.info('DO THINGS')

        # load all needed data in the pages interactions (es. login password loaded from a file using pandas)
        bot.payload.input_data = {'username': 'test', 'password': 'test', 'element_name': 'My book'}

        # Open the search page, perform actions, and go forward
        page: Page = SearchPage(bot=bot).forward()

        # For every page found, perform actions and go forward
        while page:
            page = page.forward()

        # For default, the task will succeed
        return True

    # Method executed on bot success, with its payload
    def on_success(self, payload: Payload):
        logging.info(f'SUCCESS {payload.downloads}')
    
    # Method executed on bot failure
    def on_failure(self, payload: Payload):
        logging.info(f'FAILED {payload.output_data}')

# Check if the script is executed as the main program
if __name__ == '__main__':
    # Start the above TestTask
    TestTask()()