import logging

from selenium.webdriver.remote.remote_connection import LOGGER

from fastbot import config


# libraries logging
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger('seleniumwire').setLevel(logging.WARNING)
logging.getLogger('hpack').setLevel(logging.WARNING)

LOGGER.setLevel(logging.WARNING)

logging.basicConfig(format='%(asctime)s %(filename)s:%(lineno)s - %(funcName)s - %(name)s - %(levelname)s -  %(message)s', level=config.LOG_LEVEL)