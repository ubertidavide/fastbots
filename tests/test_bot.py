import pytest

from pathlib import Path
from contextlib import nullcontext
from selenium import webdriver
from seleniumwire.webdriver import Firefox, Chrome
from selenium.webdriver.support.wait import WebDriverWait

from fastbots.bot import Bot
from fastbots.exceptions import ExpectedUrlError
from fastbots import config


@pytest.fixture
def bot_firefox():
    return Bot(config.DriverType.FIREFOX)

@pytest.fixture
def bot_chrome():
    return Bot(config.DriverType.CHROME)

class TestBot:
    def test_driver(bot):
        assert isinstance(bot.driver, webdriver) 

    def test_wait(bot):
        assert isinstance(bot.wait, WebDriverWait)

    def test_payload(bot):
        assert bot.payload == {}

    @pytest.mark.parametrize('url_to_check', 'expected_result'[
        ('https://www.amazon.com/', nullcontext),
        ('https://www.google.it/', pytest.raises(ExpectedUrlError)),
    ])
    def test_check_page_url(bot, url_to_check, expected_result):
        with expected_result:
            assert bot.check_page_url(expected_page_url=url_to_check) is not None

    @pytest.mark.parametrize('page_to_check', 'locator_to_check', 'expected_result'[
        ('search_locator', 'search_page', '(By.ID, "twotabsearchtextbox")'),
        ('product_locator', 'search_page', "(By.XPATH, '//*[@id=\"search\"]/div[1]/div[1]/div/span[1]/div[1]/div[2]')"),
        ('product_page', 'name_locator', '(By.ID, "title")'),
        ('not_exist_page', 'name_locator', pytest.raises(ValueError)),
        ('product_page', 'not_exist_locator', pytest.raises(ValueError))
    ])
    def test_locator(bot, page_to_check, locator_to_check, expected_result):
        if isinstance(expected_result, str):
            assert bot.locator(page_to_check, locator_to_check) == expected_result
        else:
            with expected_result:
                bot.locator(page_to_check, locator_to_check)

    @pytest.mark.parametrize('dowload_path_to_check', 'driver_type_to_check', 'expected_result' [
        (config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH, config.DriverType.FIREFOX, len(Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).glob('*.png'))+1),
        (config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH, config.DriverType.CHROME, len(Path(config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH).glob('*.png'))+1),
        (config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH, 'unknown_driver_type', pytest.raises(ValueError)),
        #(None, config.DriverType.FIREFOX, pytest.raises(Exception)),
    ])
    def test_save_screenshot(bot, dowload_path_to_check, driver_type_to_check, expected_result):
        config.BOT_SCREENSHOT_DOWNLOAD_FOLDER_PATH = dowload_path_to_check
        config.BOT_DRIVER_TYPE = driver_type_to_check

        if isinstance(expected_result, int):
            bot.save_screenshot()
            assert len(Path(dowload_path_to_check).glob('*.png')) == expected_result
        else:
            with expected_result:
                bot.save_screenshot()

    @pytest.mark.parametrize('dowload_path_to_check', 'driver_type_to_check', 'expected_result' [
        (config.BOT_HTML_DOWNLOAD_FOLDER_PATH, config.DriverType.FIREFOX, len(Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH).glob('*.html'))+1),
        (config.BOT_HTML_DOWNLOAD_FOLDER_PATH, config.DriverType.CHROME, len(Path(config.BOT_HTML_DOWNLOAD_FOLDER_PATH).glob('*.html'))+1),
        (config.BOT_HTML_DOWNLOAD_FOLDER_PATH, 'unknown_driver_type', pytest.raises(ValueError)),
    ])
    def test_save_html(bot, dowload_path_to_check, driver_type_to_check, expected_result):
        config.BOT_HTML_DOWNLOAD_FOLDER_PATH = dowload_path_to_check
        config.BOT_DRIVER_TYPE = driver_type_to_check

        if isinstance(expected_result, int):
            bot.save_html()
            assert len(Path(dowload_path_to_check).glob('*.html')) == expected_result
        else:
            with expected_result:
                bot.save_html()

    @pytest.mark.parametrize('dowload_path_to_check', 'driver_type_to_check', 'expected_result' [
        (config.BOT_COOKIES_FILE_PATH, config.DriverType.FIREFOX, True),
        (config.BOT_COOKIES_FILE_PATH, config.DriverType.CHROME, True),
        #(None, config.DriverType.FIREFOX, pytest.raises(Exception)),
    ])
    def test_save_cookies(bot, dowload_path_to_check, driver_type_to_check, expected_result):
        config.BOT_COOKIES_FILE_PATH = dowload_path_to_check
        config.BOT_DRIVER_TYPE = driver_type_to_check

        if isinstance(expected_result, int):
            bot.save_html()
            assert len(Path(dowload_path_to_check).glob('*.html')) == expected_result
        else:
            with expected_result:
                bot.save_html()

    def test_load_cookies():
        pass

    def test__load_locators__():
        pass

    def test___load_chrome_preferences__(bot):
        pass

    def test__load_firefox_preferences__(bot):
        pass

    def test___load_chrome_options__(bot):
        pass

    def test___load_firefox_options__(bot):
        pass

    def test___load_firefox_driver__(bot):
        assert isinstance(bot.___load_firefox_driver__(), Firefox)

    def test__load_chrome_driver__(bot):
        assert isinstance(bot.__load_chrome_driver__(), Chrome)