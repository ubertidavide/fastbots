import logging
import traceback
from abc import ABC, abstractmethod

from tenacity import RetryError, Retrying, wait_fixed, stop_after_attempt, retry_if_result, after_log

from fastbots.bot import Bot
from fastbots.chrome_bot import ChromeBot
from fastbots.firefox_bot import FirefoxBot
from fastbots import config

logger = logging.getLogger(__name__)

class Task(ABC):
    """
    Task

    A blueprint for tasks representing a series of interactions across multiple pages.

    Methods:
        run(bot: Bot) -> bool: Executes the series of interactions. Must be implemented by subclasses.
        on_success(payload): Actions to be taken on successful completion of the run method.
        on_failure(payload): Actions to be taken if the run method fails after a specified number of retries.
    """

    @abstractmethod
    def run(self, bot: Bot) -> bool:
        """
        Executes the series of interactions.

        Args:
            bot (Bot): The bot instance to perform interactions.

        Returns:
            bool: True if interactions are successful, False otherwise.

        Raises:
            NotImplementedError: Subclasses must define this method.
        """
        raise NotImplementedError('Tasks must define this method.')
    
    @abstractmethod
    def on_success(self, payload):
        """
        Actions to be taken on successful completion of the run method.

        Args:
            payload: Data collected during the run method.

        Raises:
            NotImplementedError: Subclasses must define this method.
        """
        raise NotImplementedError('Tasks must define this method.')

    @abstractmethod
    def on_failure(self, payload):
        """
        Actions to be taken if the run method fails after a specified number of retries.

        Args:
            payload: Data collected during the run method.

        Raises:
            NotImplementedError: Subclasses must define this method.
        """
        raise NotImplementedError('Tasks must define this method.')
    
    def __is_false__(self, value):
        """
        Returns True if the value is False.

        Args:
            value: The value to check.

        Returns:
            bool: True if the value is False, False otherwise.
        """
        return value is False
    
    def __call__(self):
        """
        Automatically executed when the class is instantiated and called.
        
        It executes the run method with appropriate logic and handles retries.

        Returns:
            bool: True on success, False on failure after retries.
        """
        result: bool = False
        payload: dict = {}

        try:
            for attempt in Retrying(
                wait=wait_fixed(config.BOT_RETRY_DELAY),
                stop=stop_after_attempt(config.BOT_MAX_RETRIES),
                retry=retry_if_result(self.__is_false__),
                after=after_log(logger, logging.DEBUG)
            ):
                with attempt:
                    bot: Bot = None

                    if config.BOT_DRIVER_TYPE == config.DriverType.FIREFOX:
                        bot = FirefoxBot()
                    elif config.BOT_DRIVER_TYPE == config.DriverType.CHROME:
                        bot = ChromeBot()
                    else:
                        raise ValueError(f'Unknown Driver Type: {config.BOT_DRIVER_TYPE}')

                    with bot:
                        try:
                            result = self.run(bot)
                            payload = bot.payload
                        except Exception as e:
                            result = False
                            logging.error(f'{e}')
                            logging.error(f'Full traceback: {traceback.format_exc()}')

                            try:
                                payload = bot.payload
                            except Exception as e:
                                payload = {}

                            bot.save_html()
                            bot.save_screenshot()

                if not attempt.retry_state.outcome.failed:
                    attempt.retry_state.set_result(result)

            if result:
                return self.on_success(payload)
            
        except RetryError:
            return self.on_failure(payload)
