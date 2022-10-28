from requests import Response, exceptions


class DoccanoAPIError(exceptions.HTTPError):
    def __init__(self, response: Response):
        """Initialize the exception with the response.

        Args:
            response (Response): The response to initialize the exception
        """
        super().__init__(str(response.json()), response=response)
