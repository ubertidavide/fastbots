-- main.py
# Import the logging module to handle logging in the script
import logging

# Import necessary classes and modules from the fastbots library
from fastbots import Task, Bot, Page, EC, WebElement, Keys


# Define a SearchPage class, which is a subclass of the Page class
class ProfilePage(Page):

    # Constructor to initialize the SearchPage instance
    # The page_name is used in the locators file; default is 'search_page'
    def __init__(self, bot: Bot, page_name: str = 'profile_page'):
        super().__init__(bot, page_name)

    # Define the forward method for navigating to the next page (ProductPage)
    def forward(self) -> None:
        # Log information about the current action
        logging.info('Save profile name')

        # Use locators specified in the file for flexibility and less code changes
        name_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('name_locator')))
        # Save founded data
        self.bot.payload['result'] = name_element.text

        # End the chain of page interactions
        return None

# Define a ProductPage class, which is a subclass of the Page class
class LoginPage(Page):

    # Constructor to initialize the ProductPage instance
    # The page_name is used in the locators file; default is 'product_page'
    def __init__(self, bot: Bot, page_name: str = 'login_page'): 
        super().__init__(bot, page_name)

    # Define the forward method for navigating to the next page
    def forward(self) -> ProfilePage:
        # Log information about the current action
        logging.info('Login')

        # Use locators specified in the file for flexibility and less code changes
        email_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('email_locator')))
        email_element.send_keys('test@test.com')

        password_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('password_locator')))
        password_element.send_keys('123456')

        login_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('login_locator')))
        login_element.click()

        # Continue the chain of interaction on the next page (ProfilePage)
        return ProfilePage(bot=self.bot)

# Define a TestTask class, which is a subclass of the Task class
class TestTask(Task):

    # Main task code to be executed when running the script
    def run(self, bot: Bot) -> bool:
        # Log information about the current action
        logging.info('Login and get profile info')

        # Open the search page, perform actions, and go forward
        page: Page = LoginPage(bot=bot).forward()

        # For every page found, perform actions and go forward
        while page:
            page = page.forward()

        # For default, the task will succeed
        return True

    # Method executed on bot success, with its payload
    def on_success(self, payload):
        logging.info(f'Success {payload}')
    
    # Method executed on bot failure
    def on_failure(self, payload):
        logging.info(f'Failed {payload}')

# Check if the script is executed as the main program
if __name__ == '__main__':
    # Start the above TestTask
    TestTask()()
