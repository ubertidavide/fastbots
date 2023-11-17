# fastbots
A simple library for bot development using selenium and the POM (Page Object Model) design.

## Installation:
The installation is a simple process with pip on the
PyPy repository.
```bash
pip install fastbots
```

## Showcase:
Check out the full example at the repo: [cookiecutter-fastbots](https://github.com/ubertidavide/cookiecutter-fastbots).

### Main Code
All the main code example:
```python
-- main.py
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
```

### Locators File
In the locators configuration file there is all the required locators config.
This could be changed easily without rebuild or make modifications at the code.
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

### Browser and Drivers (Optional)
For default config, the selected browser is Firefox, but it could be changed from the config file:
```ini
-- settings.ini
[settings]
#BOT_DRIVER_TYPE=FIREFOX
BOT_DRIVER_TYPE=CHROME
```
**The correct browser installed for the driver selected it's required.**
The browser installation path is autodetected by system env variables, the driver download process and it's related installation path settings are managed automatically.

### Retry and Debug (Optional)
For default every task will be retryed 2 times waiting 10 seconds, when all the two try fail, the task execute the on_error method else it will execute the on_success method.
This behaviour could be modified in the settings file:
```ini
-- settings.ini
[settings]
BOT_MAX_RETRIES=2 #sec default
BOT_RETRY_DELAY=10 #sec default
```
When the task is failed the library store the screenshot and the html of the page in the debug folder, useful for debug.
It will store also all the logs in the log.log file.

### Download Folder and other Folders (Optional)
```ini
-- settings.ini
[settings]
BOT_DOWNLOAD_FOLDER_PATH='/usr/...' #override the default download path used for the browser
BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH='/debug' # default
BOT_HTML_DOWNLOAD_FOLDER_PATH='/debug'
```

### Global Wait (Optional)
The default configured wait are showed below:
- The implicit wait used for inital page loading.
- The wait for the url check that matches the specified in the locators file
- The default wait used by the self.bot.wait function
```ini
-- settings.ini
[settings]
SELENIUM_GLOBAL_IMPLICIT_WAIT=5 #sec default
SELENIUM_EXPECTED_URL_TIMEOUT=5 #sec default
SELENIUM_DEFAULT_WAIT=5 #sec default

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
Configure Firefox Arguments, store them in the config file, the format it's the same for all the supported drivers, check carefully that the exact arg it's implemented for the selected driver.

#### Firefox args:
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
Store preferences in a json file, the format it's the same for all the supported drivers, check carefully that the exact string and value it's implemented for the selected driver.

#### Firefox prefs:
```json
-- preferences.json 
{
    "browser.download.manager.showWhenStarting": false, # Don't show download
    "browser.helperApps.neverAsk.saveToDisk": "application/pdf" # Automatic save pdf files
}
```

#### Chrome prefs:
```json
-- preferences.json 
{
    "profile.default_content_setting_values.notifications": 2,  # Disable notifications
    "profile.default_content_settings.popups": 0  # Allow popups
}
```