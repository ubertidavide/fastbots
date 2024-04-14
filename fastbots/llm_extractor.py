from typing import List
import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel

from fastbots.bot import Bot
from fastbots import config


class LLMExtractor(object):
    """
    LLM Extractor

    This is an extractor utility useful for leveraging the llm ability to extract automatically data from html.
    The data must be explained throught a pydantic model, this extractor use the rule to parse and validate correctly
    the needed entities.
    It uses an OpenAI llm model.

    Attributes:
        _bot (Bot): The bot instance associated with the extractor.
        _pydantic_model (BaseModel): The representation of the data needed to extract and validate the parsed data.

    Methods:
        __init__(self, bot: Bot, pydantic_model: BaseModel): Initialized the LLMExtractor class.
        extract_data(self, locator_name: str) -> str: Extract the needed data.
    """

    def __init__(self, bot: Bot, pydantic_model: BaseModel) -> None:
        """
        Initializes the LLMExtractor class.

        Args:
            bot (Bot): The bot instance associated with the extractor.
            pydantic_model (BaseModel): The representation of the data needed to extract and validate the parsed data.
        """
        super().__init__()

        self._bot: Bot = bot

        llm_model = ChatOpenAI(
            temperature=0, 
            model="gpt-3.5-turbo", 
            openai_api_key=config.OPENAI_API_KEY
        )

        prompt_template = """ given this information {information} of an entity on this piece of html,
            I want you to extract all the information about this entity.
            You are not allowed to make any assumptions while extracting the information.
            Every link you provide should be from the information given.
            There should be no assumptions for Links/URLS.
            You should not return code to do it.:
            You should extract the following text infromation from the html:
            \n{format_instructions} # here we are passing format_instructions
        """

        json_output_parser = JsonOutputParser(
            pydantic_model=pydantic_model
        )

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["information"],
            partial_variables={"format_instructions": json_output_parser.get_format_instructions()},
        )

        self._llm_chain = LLMChain(llm=llm_model, prompt=prompt)

    def __locator__(self, locator_name: str) -> tuple:
        """
        Utility method to load a locator.

        The locators in the file must be in the format:
        [llm_extractor]
        locator_name=(By.XPATH, "//html//input")

        Args:
            locator_name (str): The name of the locator.

        Returns:
            tuple: A tuple representing the loaded locator.

        Raises:
            ValueError: If the locator is not enclosed in round brackets or is of an unknown or incorrect format.
        """
        # load the locators from file and interpret that as code
        full_locator: str = self._bot.locator('llm_extractor', locator_name).strip().replace('\\\'',  '\'').replace('\\"', '"')

        if not full_locator.startswith('(') or not full_locator.endswith(')'):
            raise ValueError('The locator must be enclosed in round brackets.')

        # declared locators
        locator_list: List[str] = [
            'By.ID', 'By.XPATH', 'By.NAME', 'By.CLASS_NAME', 'By.CSS_SELECTOR', 
            'By.LINK_TEXT', 'By.PARTIAL_LINK_TEXT', 'By.TAG_NAME'
        ]

        # check the used locator
        parsed_locator: tuple = None
        for locator in locator_list:
            # check that the first characters are them of the locators and the next one of the comma 
            if full_locator[1:-1].strip().startswith(locator) and full_locator[1:-1].strip()[len(locator):].strip().startswith(','):
                # extract the tuple required as locator
                parsed_locator = (
                    eval(locator), 
                    full_locator[1:-1].strip()[len(locator):].strip()[1:].strip()[1:-1]
                )

                logging.debug(f'{locator_name} {parsed_locator}')

                return parsed_locator
            
        else:
            raise ValueError('The specified locator is unknown or wrong; check by, brackets, and commas.')

    def extract_data(self, locator_name: str) -> str:
        """
        Extract the data as a json string, validated throught the data format specified by the pydantic model.

        The locators in the file must be in the format:
        [llm_extractor]
        locator_name=(By.XPATH, "//html//input")

        Args:
            locator_name (str): The name of the locator.
        """
        try:
            extracted_data = self._llm_chain.invoke(
                input={"information": self._bot.wait.until(EC.presence_of_element_located(self.__locator__(locator_name))).get_attribute('innerHTML')},
                return_only_outputs=True,
            )
            return extracted_data["text"]
        except Exception as e:
            logging.error(e)
            return None