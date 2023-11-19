import pytest
import configparser
from pathlib import Path

from selenium import webdriver
from seleniumwire.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions

from fastbots.chrome_bot import ChromeBot
from fastbots.exceptions import ExpectedUrlError
from fastbots import config


@pytest.fixture
def bot():
    return ChromeBot()


def test_driver(bot):
    assert isinstance(bot.driver, webdriver) 

def test_wait(bot):
    assert isinstance(bot.wait, WebDriverWait)

def test_payload(bot):
    assert bot.payload == {}

"""@pytest.mark.parametrize('url_to_check', 'expected_result', [
    ('https://www.amazon.com/', None),
    ('https://www.google.it/', pytest.raises(ExpectedUrlError)),
])
def test_check_page_url(url_to_check, expected_result, request):
    bot = request.getfixturevalue(bot)

    if expected_result is None:
        bot.check_page_url(expected_page_url=url_to_check) 
    else:
        with expected_result:
            bot.check_page_url(expected_page_url=url_to_check)

@pytest.mark.parametrize('page_to_check', 'locator_to_check', 'expected_result', [
    ('search_locator', 'search_page', '(By.ID, "twotabsearchtextbox")'),
    ('product_locator', 'search_page', "(By.XPATH, '//*[@id=\"search\"]/div[1]/div[1]/div/span[1]/div[1]/div[2]')"),
    ('product_page', 'name_locator', '(By.ID, "title")'),
    ('not_exist_page', 'name_locator', pytest.raises(ValueError)),
    ('product_page', 'not_exist_locator', pytest.raises(ValueError))
])
def test_locator(page_to_check, locator_to_check, expected_result, request):
    bot = request.getfixturevalue(bot)

    if isinstance(expected_result, str):
        assert bot.locator(page_to_check, locator_to_check) == expected_result
    else:
        with expected_result:
            bot.locator(page_to_check, locator_to_check)"""

def test_save_screenshot(bot):
    expected_result = len(Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).glob('*.png'))+1
    bot.save_screenshot()
    assert len(Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).glob('*.png')) == expected_result

def test_save_html(bot):
    expected_result = len(Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH).glob('*.html'))+1
    bot.save_html()
    assert len(Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH).glob('*.html')) == expected_result

def test_save_cookies(bot):
    bot.save_cookies()
    assert Path(config.BOT_COOKIES_FILE_PATH).is_file()

def test_load_cookies(bot):
    bot.save_cookies()
    assert bot.load_cookies() == bot.driver.get_cookies()

"""def test__load_locators__(bot):
    assert isinstance(bot.__load_locators__(), configparser)

def test___load_preferences__(bot):
    assert isinstance(bot.__load_preferences__(), dict)
    #TODO: check that all the preferences are loaded correctly (default and files)

def test___load_options__(bot):
    assert isinstance(bot.___load_options__(), ChromeOptions)
    #TODO: check that all the option are loaded correctly (default and files)

def test___load_driver__(bot):
    assert isinstance(bot.___load_firefox_driver__(), Chrome)
    #TODO: check that all the config are loaded correctly (default and files)"""