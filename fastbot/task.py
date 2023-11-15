import logging
from abc import ABC, abstractmethod

from tenacity import Retrying, wait_fixed, stop_after_attempt, retry_if_result, after_log

from fastbot.bot import Bot
from fastbot.exceptions import GenericError


logger = logging.getLogger(__name__)


class Task(ABC):
    """
    Task

    A Task blueprint that need to implement the three below specified methods.
    It is a class needed to rapresent a full interaction over more pages.
    """

    #: Maximum number of retries before giving up.  If set to :const:`None`,
    #: it will **never** stop retrying.
    max_retries = 2

    #: Default time in seconds before a retry of the task should be
    #: executed. 5 sec by default.
    default_retry_delay = 5

    @abstractmethod
    def run(self, bot: Bot) -> bool:
        """
        Run

        This method it's called when the class is istantiated, don't call
        them directly, used for blueprint of a series of interaction with
        different pages in order to make a complete navigation.
        """
        raise NotImplementedError('Tasks must define this method.')
    
    @abstractmethod
    def on_success(self):
        """
        On Success

        This method is executed automatically only if the run
        method is runned whitout problems.
        """
        raise NotImplementedError('Tasks must define this method.')

    @abstractmethod
    def on_failure(self, retry_state):
        """
        On Failure

        This method is executed automatically only if the run
        method is runned with problems for a specified series of times.
        """
        raise NotImplementedError('Tasks must define this method.')
    
    def __is_false__(self, value):
        """Return True if value is False"""
        return value is False
    
    def __call__(self):
        """
        This method is runned automatically when this class it's istantiated
        and called, it will execute the run method with all it' correct logic.
        """
        result: bool = False

        for attempt in Retrying(wait=wait_fixed(Task.default_retry_delay),
                                stop=stop_after_attempt(Task.max_retries),
                                retry=retry_if_result(self.__is_false__),
                                retry_error_callback=self.on_failure,
                                after=after_log(logger, logging.DEBUG)):
            with attempt:
                with Bot() as bot:
                    try:
                        result: bool = self.run(bot)
                    except Exception as e:
                        result: bool = False
                        logging.error(f'{e}')

            if not attempt.retry_state.outcome.failed:
                attempt.retry_state.set_result(result)

        if result:
            return self.on_success()