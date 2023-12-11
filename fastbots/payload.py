from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Payload:
    """
    Payload class for managing input data, downloads, and output data.
    """

    def __init__(self):
        """
        Initialize an instance of the Payload class.
        """
        # Private variables with double underscores
        self.__input_data: Dict[str, str] = field(default_factory=dict)
        self.__downloads: List[str] = field(default_factory=list)
        self.__output_data: Dict[str, str] = field(default_factory=dict)

    @property
    def input_data(self):
        """
        Get the input data.

        Returns:
            dict: The input data.
        """
        return self.__input_data

    @input_data.setter
    def input_data(self, data):
        """
        Set the input data.

        Args:
            data (dict): The input data to set.
        """
        self.__input_data = data

    @property
    def downloads(self):
        """
        Get the list of downloads.

        Returns:
            list: The list of download paths.
        """
        return self.__downloads

    @downloads.setter
    def downloads(self, data):
        """
        Set the list of downloads.

        Args:
            data (list): The list of download paths to set.
        """
        self.__downloads = data

    @property
    def output_data(self):
        """
        Get the output data.

        Returns:
            dict: The output data.
        """
        return self.__output_data

    @output_data.setter
    def output_data(self, data):
        """
        Set the output data.

        Args:
            data (dict): The output data to set.
        """
        self.__output_data = data