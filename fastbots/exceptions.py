class GenericError(Exception):
    """ 
    Generic Error
    
    Represents a generic error.

    Attributes:
        message (str): The error message.

    Methods:
        __init__(message: str = 'Generic Error'): Initializes the GenericError instance.
        __str__(): Returns the error message as a string.

    Example:
        ```python
        try:
            # Some code that may raise a GenericError
        except GenericError as e:
            print(f"Caught an error: {e}")
        ```
    """

    def __init__(self, message: str = 'Generic Error') -> None:
        """
        Initializes the GenericError instance.

        Args:
            message (str): The error message.
        """
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        Returns the error message as a string.

        Returns:
            str: The error message.
        """
        return self.message

class ExpectedUrlError(GenericError):
    """ 
    Expected Url Error

    Occurs when the current URL is not the expected one. 

    Attributes:
        current_url (str): The current URL of the browser.
        expected_url (str): The expected URL.

    Methods:
        __init__(current_url: str, expected_url: str): Initializes the ExpectedUrlError instance.
        __str__(): Returns the error message as a string.

    Example:
        ```python
        try:
            # Some code that may raise an ExpectedUrlError
        except ExpectedUrlError as e:
            print(f"Caught an error: {e}")
        ```
    """
    
    def __init__(self, current_url: str, expected_url: str) -> None:
        """
        Initializes the ExpectedUrlError instance.

        Args:
            current_url (str): The current URL of the browser.
            expected_url (str): The expected URL.
        """
        self.current_url: str = current_url
        self.expected_url: str = expected_url
        self.message: str = f'The current URL: {self.current_url} of the browser is not the expected: {self.expected_url}'
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        Returns the error message as a string.

        Returns:
            str: The error message.
        """
        return self.message
    
class DownloadFileError(GenericError):
    """
    Download File Error

    Occurs when an error occurs in the downloading process.

    Attributes:
        message (str): The error message.

    Methods:
        __init__(message: str = 'Download File Error'): Initializes the DownloadFileError instance.
        __str__(): Returns the error message as a string.

    Example:
        ```python
        try:
            # Some code that may raise a DownloadFileError
        except DownloadFileError as e:
            print(f"Caught an error: {e}")
        ```
    """

    def __init__(self, message: str = 'Download File Error') -> None:
        """
        Initializes the DownloadFileError instance.

        Args:
            message (str): The error message.
        """
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        Returns the error message as a string.

        Returns:
            str: The error message.
        """
        return self.message
