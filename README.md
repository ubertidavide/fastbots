# fastbots
[Fastbots](https://ubertidavide.github.io/fastbots/) is a simple library designed for rapid bot and scraper development using Selenium and the POM (Page Object Model) design.  
It enhances productivity by allowing developers to focus solely on scraping, reducing boilerplate code, and eliminating the need for direct driver management-related code, thanks to browser-independent settings.  
Even if site locators change, this library doesn't require modifications to the code; adjustments can be made solely in the configuration.  

fastbots is also fully compatible with all selenium functions, refer to [selenium official documentation](https://www.selenium.dev/documentation/webdriver/elements/interactions/) for more details.

## Installation
The installation process is straightforward using pip from the PyPI repository.

```bash
pip install fastbots
```

## Showcase
Check out the full example at the: [cookiecutter-fastbots](https://github.com/ubertidavide/cookiecutter-fastbots).

### Main Code
Here's the main code example:
```python
-- main.py
# Import the logging module to handle logging in the script
import logging

# Import necessary classes and modules from the fastbots library
from fastbots import Task, Bot, Page, EC, WebElement, Keys, ActionChains, Select, Alert, TimeoutException, NoSuchElementException

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
        name_element: WebElement = self.bot.wait.until(EC.element_to_be_clickable(self.__locator__('name_locator')))
        
        # Store data in the payload section for future retrieval on success
        self.bot.payload['result'] = name_element.text

        # example of downloading the product png images and rename it (check download folder settings)
        # name_element.click() for example on element download button
        # self.bot.wait_downloaded_file_path("png", new_name_file=self.bot.payload['data']['element_name'])

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
        search_element.send_keys(self.bot.payload['data']['element_name'])
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

        # load all needed data in the interactions (es. login password)
        self.bot.payload['data']['element_name'] = 'test'

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
```

### Locators File
In the locators configuration file, all required locator configurations are defined. 
This can be easily changed without rebuilding or making modifications to the code.
```ini
-- locators.ini
[pages_url] # pages_url required url settings
start_url=https://www.amazon.com/ #start_url it's the first page driver.get()
search_page=https://www.amazon.com/ #*_page it's the first page url used for the page_name parameter with it's url that need to match
product_page=https://www.amazon.com/s?k=Selenium+with+Python#*_page it's the second page url used for the page_name parameter with it's url that need to match

[search_page] #*_page first page_name parameter, with it's related locators
search_locator=(By.ID, "twotabsearchtextbox")
product_locator=(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]')

[product_page]#*_page second page_name parameter, with it's related locators
name_locator=(By.ID, "title")
```

## Settings


### Browser and Drivers (Optional)
For default configuration, the selected browser is Firefox, but it could be changed from the config file:
```ini
-- settings.ini
[settings]
#BOT_DRIVER_TYPE=FIREFOX
BOT_DRIVER_TYPE=CHROME
```
**The correct browser installed for the driver selected is required**.
The browser installation path is autodetected by system environment variables, and the driver download process and its related installation path settings are managed automatically.

### Retry and Debug (Optional)
By default, every task will be retried 2 times, waiting for 10 seconds. If all two attempts fail, the task executes the on_error method; otherwise, it will execute the on_success method. This behavior could be modified in the settings file:
This behaviour could be modified in the settings file:
```ini
-- settings.ini
[settings]
BOT_MAX_RETRIES=2 #sec default
BOT_RETRY_DELAY=10 #sec default
```
When the task fails, the library stores the screenshot and the HTML of the page in the debug folder, useful for debugging. It will also store all the logs in the log.log file.

### Page Url Check (Automatic)
Every defined page must have a page URL, and when it's instantiated and reached by the bot, the library checks that the specified URL in the config matches the reached page during navigation to reduce navigation errors. If you want to disable this function, see the Global Wait Section below.

### File Download Wait (Functions)
This library has the bot.wait_downloaded_file_path(file_extension, new_name_file=None) method that could be used after a button download click to wait and get the path of the downloaded file. It will also give the ability to rename the file. The extension is used to check that the downloaded file is correct and not corrupted.

### Download Folder and other Folders (Optional)
```ini
-- settings.ini
[settings]
BOT_DOWNLOAD_FOLDER_PATH='/usr/...' #override the default download path used for the browser
BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH='/debug' # default
BOT_HTML_DOWNLOAD_FOLDER_PATH='/debug'
```

### Global Wait (Optional)
The default configured waits are shown below:
- The implicit wait used for initial page loading.
- The wait for the URL check that matches the specified in the locators file.
- The default wait used by the self.bot.wait function.
```ini
-- settings.ini
[settings]
SELENIUM_GLOBAL_IMPLICIT_WAIT=5 #sec default
SELENIUM_EXPECTED_URL_TIMEOUT=5 #sec default
SELENIUM_DEFAULT_WAIT=5 #sec default
SELENIUM_FILE_DOWNLOAD_TIMEOUT=20 #sec default

SELENIUM_EXPECTED_URL_CHECK=False #disable the automatic page url check, the default value it's True
```

### Proxy (Optional)
Configure the proxy settings.
```ini
-- settings.ini
[settings]
BOT_PROXY_ENABLED=True
BOT_HTTP_PROXY=127.0.0.1:8080
BOT_HTTPS_PROXY=127.0.0.1:8080
```

### User Agent (Optional)
Configure the user agent used for the requests.
```ini
-- settings.ini
[settings]
BOT_USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
```

### Arguments (Optional)
Configure Firefox Arguments, store them in the config file. The format is the same for all the supported drivers; check carefully that the exact arg is implemented for the selected driver.

#### Firefox args
```ini
-- settings.ini
[settings]
BOT_ARGUMENTS=["--headless", "--disable-gpu"]
```

#### Chrome args
```ini
-- settings.ini
[settings]
BOT_ARGUMENTS=["--no-sandbox"]
```

### Store Preferences (Optional)
Store preferences in a JSON file, the format is the same for all the supported drivers; check carefully that the exact string and value are implemented for the selected driver.

#### Firefox prefs
```jsonc
-- preferences.json 
{
    "browser.download.manager.showWhenStarting": false, # Don't show download
    "browser.helperApps.neverAsk.saveToDisk": "application/pdf" # Automatic save PDF files
}
```

#### Chrome prefs
```jsonc
-- preferences.json 
{
    "profile.default_content_setting_values.notifications": 2,  # Disable notifications
    "profile.default_content_settings.popups": 0  # Allow popups
}
```

### References
[Fastbots docs](https://ubertidavide.github.io/fastbots/)
