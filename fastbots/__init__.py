from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException

import capsolver

from langchain_core.pydantic_v1 import BaseModel, Field

from fastbots.bot import Bot
from fastbots.page import Page
from fastbots.task import Task
from fastbots.payload import Payload
from fastbots.llm_extractor import LLMExtractor
