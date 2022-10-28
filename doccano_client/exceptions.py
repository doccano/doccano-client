from requests import Response, exceptions


class DoccanoAPIError(exceptions.HTTPError):
    def __init__(self, message: str, response: Response):
        """Initialize the exception with the response.

        Args:
            message (str): The error message
            response (Response): The response to initialize the exception
        """
        try:
            super().__init__(str(response.json()), response=response)
        except exceptions.JSONDecodeError:
            super().__init__(message, response=response)
