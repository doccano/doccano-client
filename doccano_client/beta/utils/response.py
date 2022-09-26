from requests import Response, exceptions


class DoccanoAPIError(exceptions.HTTPError):
    def __init__(self, response: Response):
        """Initialize the exception with the response."""
        super().__init__(str(response.json()), response=response)


def verbose_raise_for_status(response: Response) -> None:
    """Output a bad response's text before raising for verbosity, return response otherwise"""
    try:
        response.raise_for_status()
    except exceptions.HTTPError as err:
        raise DoccanoAPIError(err.response)

    return response
