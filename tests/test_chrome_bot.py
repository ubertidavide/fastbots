import pytest
from configparser import ConfigParser
from pathlib import Path

from seleniumwire.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from fastbots.chrome_bot import ChromeBot
from fastbots import config, Payload


@pytest.fixture()
def bot():
    with ChromeBot() as bot:
        yield bot


def test_driver(bot):
    assert isinstance(bot.driver, WebDriver) 

def test_wait(bot):
    assert isinstance(bot.wait, WebDriverWait)

def test_payload(bot):
    assert isinstance(bot.payload, Payload)

def test_locator(bot):
    assert bot.locator('search_page', 'search_locator') == '(By.ID, "twotabsearchtextbox")'
    assert bot.locator('search_page', 'search_locator') == '(By.ID, \'twotabsearchtextbox\')'
    assert bot.locator('search_page', 'search_locator') == "(By.ID, 'twotabsearchtextbox')"
    assert bot.locator('search_page', 'search_locator') == "(By.ID, \"twotabsearchtextbox\")"

    with pytest.raises(ValueError):
        bot.locator('product_page', 'not_exist_locator')

    with pytest.raises(ValueError):
        bot.locator('not_exist_page', 'name_locator')

def test_save_screenshot(bot):
    expected_result = len(list(Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).glob('*.png')))+1
    bot.save_screenshot()
    assert len(list(Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).glob('*.png'))) == expected_result

def test_save_html(bot):
    expected_result = len(list(Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH).glob('*.html')))+1
    bot.save_html()
    assert len(list(Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH).glob('*.html'))) == expected_result

def test_save_cookies(bot):
    bot.save_cookies()
    assert Path(config.BOT_COOKIES_FILE_PATH).is_file()

def test_load_cookies(bot):
    expected_result = bot.driver.get_cookies()
    bot.save_cookies()
    bot.load_cookies()
    assert bot.driver.get_cookies() == expected_result

def test__load_locators__(bot):
    assert isinstance(bot.__load_locators__(), ConfigParser)

def test___load_preferences__(bot):
    assert isinstance(bot.__load_preferences__(), dict)
    #TODO: check that all the preferences are loaded correctly (default and files)

def test___load_options__(bot):
    assert isinstance(bot.__load_options__(), ChromeOptions)
    #TODO: check that all the option are loaded correctly (default and files)

def test___load_driver__(bot):
    assert isinstance(bot.__load_driver__(), Chrome)
    #TODO: check that all the config are loaded correctly (default and files)"""