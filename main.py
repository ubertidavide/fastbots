from typing import Type
from fastbot import Task, Bot, Page

import time
import logging


class SearchPage(Page):

    def __init__(self, bot: Bot, page_name: str = 'page_name'):
        super().__init__(bot, page_name)

    def forward(self) -> Type[Page] | None:
        logging.info('DO THINGS')
        search_bar = self.bot.driver.find_element(*self.__locator__('locator_name'))
        logging.info(f'Searchbar: {search_bar.is_enabled}')
        return None

class TestTask(Task):

    def run(self, bot: Bot) -> bool:
        time.sleep(5)
        SearchPage(bot, page_name='page_name').forward()
        time.sleep(5)
        return True

    def on_success(self):
        logging.info('SUCCESS')
    
    def on_failure(self, retry_state):
        logging.info('FAILED')
        
if __name__ == '__main__':
    TestTask()()