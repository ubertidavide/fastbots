import logging
from logging.handlers import RotatingFileHandler

from selenium.webdriver.remote.remote_connection import LOGGER

from fastbots import config


# Configure logging for external libraries
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger('seleniumwire').setLevel(logging.WARNING)
logging.getLogger('hpack').setLevel(logging.WARNING)

# Set logging level for Selenium remote connection
LOGGER.setLevel(logging.WARNING)

# Configure root logger with console and file handlers
logging.basicConfig(
    handlers=[logging.StreamHandler(), RotatingFileHandler('log.log', maxBytes=2000)],
    format='%(asctime)s %(filename)s:%(lineno)s - %(funcName)s - %(name)s - %(levelname)s -  %(message)s',
    level=config.LOG_LEVEL
)
