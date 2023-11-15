class GenericError(Exception):
    """ Generic Error """
    
    def __init__(self, message: str = 'Generic Error') -> None:
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

class ExpectedUrlError(GenericError):
    """ 
    Expected Url Error

    Happen when the current url is not the expected. 
    """
    
    def __init__(self, current_url: str, expected_url: str) -> None:
        self.current_url: str = current_url
        self.expected_url: str = expected_url
        self.message: str = f'The current url: {self.current_url} of the browser is not the expected: {self.expected_url}'
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
