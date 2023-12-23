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

Check out the full template example at [cookiecutter-fastbots](https://github.com/ubertidavide/cookiecutter-fastbots), improve the development speed with this ready to use template, reducing the boilerplate code.

### Main Code

Here's the main code example:

```python
# main.py
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
        page: Page = SearchPage(bot=bot)

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
```

**Attention**: This framework is flexible, you could also use only the Task class and the selenium's related functions inside the run method without using the POM (Page Object Model) or develop specific pages flow depending on your needs.

### Locators File

In the locators configuration file `locators.ini`, all required locator configurations are defined.  
This can be easily changed without rebuilding or making modifications to the code.  
It provides a structured and well-known way of managing page locators and urls, useful for scalability in big projects.

```ini
# locators.ini
[pages_url] # pages_url required url settings
start_url=https://www.amazon.com/ #start_url it's the first page driver.get() could be also None
search_page=https://www.amazon.com/ #*_page it's the first page url used for the page_name parameter with it's url that need to match
product_page=None#Used to skip the page_url check of the current url on a single page

[search_page] #*_page first page_name parameter, with it's related locators
search_locator=(By.ID, "twotabsearchtextbox")
product_locator=(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]')

[product_page]#*_page second page_name parameter, with it's related locators
name_locator=(By.ID, "title")
```

## Settings

### Browser and Drivers 

For default configuration, the selected browser is Firefox, but it could be changed from the `settings.ini` file:

```ini
# settings.ini
[settings]
#BOT_DRIVER_TYPE=FIREFOX
BOT_DRIVER_TYPE=CHROME
```

**The correct browser installed for the driver selected is required**.
The browser installation path is autodetected by system environment variables, and the driver download process and its related installation path settings are managed automatically.

### Retry and Debug 

By default, every task will be retried 2 times, waiting for 10 seconds. If all two attempts fail, the task executes the `on_error` method; otherwise, if the `run` fuction will `return True`, then it will be executed the `on_success` method.  
This behaviour could be modified in the settings file:

```ini
# settings.ini
[settings]
BOT_MAX_RETRIES=2 #sec default
BOT_RETRY_DELAY=10 #sec default
```

When the task fails, the library stores the screenshot and the HTML of the page in the debug folder, useful for debugging.  

```ini
# settings.ini
[settings]
BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH='/debug' # default
BOT_HTML_DOWNLOAD_FOLDER_PATH='/debug' # default
```

It will also store all the logs in the `log.log` file.

### Page Url Check

#### Strict Page Check (Default)
During the navigation the driver goes througth different pages, in every pages initialization, in the default behaviour, the url of the browsers and the specified url of the page setted in the `locators.ini` are cheched.  
There is also the possibility to change the `page_url` check type from `strict_page_url` (exact match), with the current url that need to contains the page url, setting `strict_page_url=False`, in the page `__init__` method after the page name.

#### Disabled Strict Page Check
This check could be disabled globally setting `SELENIUM_EXPECTED_URL_CHECK` to `False` or on a specific page in the `locators.ini` file, at the `[page_url]` section, setting `page_name=None`.

```ini
# settings.ini
[settings]
SELENIUM_EXPECTED_URL_CHECK=False #disable the automatic page url check, the default value it's True
```

### File Download

Specify the path used to store the downloaded files.

```ini
# settings.ini
[settings]
BOT_DOWNLOAD_FOLDER_PATH='/usr/...' #override the default download path used for the browser
```

#### Strict Download Wait (Default)

This library has the `bot.wait_downloaded_file_path(file_extension, new_name_file=None)` method that could be used after a click on a file download button, to wait and get the path of the downloaded file.  
It will give also the ability to rename the file.  
The file extension is used to check that the downloaded file is correct and not corrupted.  
It's the default behaviour, all the downloaded file need to be waited to be moved to download folder, to change this, disable strict download wait in the config, see the next section.

#### Disabled Strict Download Wait

At the end of the `run` Task method all the downloaded files are moved to the download folder.

```ini
# settings.ini
[settings]
BOT_STRICT_DOWNLOAD_WAIT=True #default, False -> all the downloaded file are move to download folder always without wait check
```

### Wait Managment

The default configured waits are shown below:

- `SELENIUM_GLOBAL_IMPLICIT_WAIT`: The global [implicit](https://selenium-python.readthedocs.io/waits.html#implicit-waits) wait.

- `SELENIUM_EXPECTED_URL_TIMEOUT`: The automatic waited time for the URL check to match a specific condition, done when the page is initialized.  

- `SELENIUM_DEFAULT_WAIT`: The default waited time used by the `bot.wait` function (A WebDriverWait ready to use).

- `SELENIUM_FILE_DOWNLOAD_TIMEOUT`: The default waited file download time used by the `bot.wait_downloaded_file_path()`

```ini
# settings.ini
[settings]
SELENIUM_GLOBAL_IMPLICIT_WAIT=5 #sec default
SELENIUM_EXPECTED_URL_TIMEOUT=5 #sec default
SELENIUM_DEFAULT_WAIT=5 #sec default
SELENIUM_FILE_DOWNLOAD_TIMEOUT=20 #sec default
```

### Proxy, Rotating Proxies, Web Unlocker Support 

Configure the proxy settings, you could proxy to a specific IP:

```ini
# settings.ini
# '<proxy_protocol>://<username>:<password>@<proxy_ip_address>:<proxy_port>'
[settings]
BOT_PROXY_ENABLED=True
BOT_HTTP_PROXY=127.0.0.1:8080
BOT_HTTPS_PROXY=127.0.0.1:8080
```

or even to a paid proxy service like [Brightdata](https://brightdata.com/proxy-types/residential-proxies), [Oxylabs](https://oxylabs.io/products/residential-proxy-pool), [Netnut](https://netnut.io/rotating-residential-proxies/) that let you connect throught different IPs and help bypass CAPTCHA with the web unlocker solution:

```ini
# settings.ini Oxyslab
# 'http://{username}:{password}@{proxy}'
[settings]
BOT_PROXY_ENABLED=True
BOT_HTTP_PROXY=http://customer-USER:PASS@pr.oxylabs.io:7777
BOT_HTTPS_PROXY=http://customer-USER:PASS@pr.oxylabs.io:7777
```

**Attention** : All your data will pass through the proxy, check that the proxy is a trusted source before you use them.

### CAPTCHA Solvers

By default, this library integrate [capsolver](https://docs.capsolver.com/guide/getting-started) service, this provide the possibility to bypass an high number of different CAPTCHAs.

An example code:

```python
from fastbots import capsolver

solution = capsolver.solve({
        "type":"ReCaptchaV2TaskProxyLess",
        "websiteKey":"6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        "websiteURL":"https://www.google.com/recaptcha/api2/demo",
    })

print(solution)
```

Specify your API Key in the settings.

```ini
# settings.ini
[settings]
CAPSOLVER_API_KEY="my-api-key"
```

For more and detailed capabilities see [capsolver](https://docs.capsolver.com/guide/getting-started) official docs.

### User Agent 

Configure the user agent used for the requests, for default it will be fastbots.

```ini
# settings.ini
[settings]
BOT_USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
```

For more or specific user agents see [this list](https://www.useragents.me/).

### Arguments and Profiles

Configure Firefox Arguments, store them in the config file. The format is the same for all the supported drivers; check carefully that the exact arg is implemented for the selected driver.  
Arguments are also used to load specific profiles already created, see driver related docs [Firefox Profile Manager](https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles), [Firefox Profile](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data), [Chrome Profile](https://support.google.com/chrome/answer/2364824)

#### Firefox args

```ini
# settings.ini
[settings]
BOT_ARGUMENTS="-headless, -profile ./selenium"
```

For a detailed list of all supported args check [Firefox Args](https://wiki.mozilla.org/Firefox/CommandLineOptions)

#### Chrome args

```ini
# settings.ini
[settings]
BOT_ARGUMENTS="--headless, --disable-gpu, --no-sandbox, --user-data-dir=./selenium, --profile-directory=selenium"
```

For a detailed list of all supported args check [Chromium Args](https://peter.sh/experiments/chromium-command-line-switches/).

### Store Preferences

Store preferences in a JSON file, the format is the same for all the supported drivers; check carefully that the exact string and value are implemented for the selected driver.

#### Firefox prefs

```jsonc
// preferences.json
{
  "browser.download.manager.showWhenStarting": false, // Don't show download
  "browser.helperApps.neverAsk.saveToDisk": "application/pdf", // Automatic save PDF files
  "pdfjs.disabled": true // Don't show the pdf
}
```

For a detailed list of all supported prefs check [Firefox Profile Prefs](https://searchfox.org/mozilla-release/source/browser/app/profile/firefox.js) and [Firefox All Prefs](https://searchfox.org/mozilla-release/source/modules/libpref/init/all.js)

#### Chrome prefs

```jsonc
// preferences.json
{
  "profile.default_content_setting_values.notifications": 2, // Disable notifications
  "profile.default_content_settings.popups": 0 // Allow popups
}
```

For a detailed list of all supported prefs check [Chrome Prefs](https://src.chromium.org/viewvc/chrome/trunk/src/chrome/common/pref_names.cc?view=markup)

### Cookies Managment

There is also the possibility to load `bot.load_cookies()` and store `bot.save_cookies()` cookies from file.

```ini
# settings.ini
[settings]
BOT_COOKIES_FILE_PATH=cookies.pkl #default
```

### Interceptor

This library integrate also the selenium-wire capabilities, traffic capture is disabled by default.

```ini
# settings.ini
[settings]
# enable capture
SELENIUM_DISABLE_CAPTURE=False
# capture only in scope requests and response (comma separated list of domains)
SELENIUM_IN_SCOPE_CAPTURE='.*stackoverflow.*, .*github.*'
# enalbe HAR capture
SELENIUM_ENABLE_HAR_CAPTURE=True
```

#### Response Interceptor

```python
def interceptor(request, response):  # A response interceptor takes two args
    # add a header to some domain
    if request.url == 'https://server.com/some/path':
        response.headers['New-Header'] = 'Some Value'

bot.driver.response_interceptor = interceptor
```

#### Request Interceptor

```python
def interceptor(request): # A response interceptor take one args

    # Block PNG, JPEG and GIF images
    if request.path.endswith(('.png', '.jpg', '.gif')):
        request.abort()
    
    # add parameter
    params = request.params
    params['foo'] = 'bar'
    request.params = params

bot.driver.request_interceptor = interceptor
```

See [selenium-wire](https://github.com/wkeeling/selenium-wire) docs for more detailed use cases.

### References

[Fastbots docs](https://ubertidavide.github.io/fastbots/)
