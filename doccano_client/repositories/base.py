import requests
from requests import Response, exceptions


class DoccanoAPIError(exceptions.HTTPError):
    def __init__(self, response: Response):
        """Initialize the exception with the response.

        Args:
            response (Response): The response to initialize the exception
        """
        super().__init__(str(response.json()), response=response)


def verbose_raise_for_status(response: Response) -> Response:
    """Output a bad response's text before raising for verbosity, return response otherwise.

    Args:
        response (Response): The response to raise for status

    Returns:
        Response: The response

    Raises:
        DoccanoAPIError: if request raises HTTPError.
    """
    try:
        response.raise_for_status()
    except exceptions.HTTPError as err:
        raise DoccanoAPIError(err.response)
    return response


class BaseRepository:
    """Base repository for interacting with the Doccano API"""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._session = requests.Session()
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "referer": base_url,
        }
        self._session.headers.update(headers)

    @property
    def login_url(self) -> str:
        """Retrieve an API login url based on the base_url

        Returns:
            str: The login url
        """
        return f"{self._base_url}/v1/auth/login/"

    @property
    def api_url(self) -> str:
        """Retrieve an API url based on the base_url

        Returns:
            str: The API url
        """
        return f"{self._base_url}/v1"

    def login(self, username: str, password: str) -> None:
        """Login to a session with the Doccano instance related to the base url

        Args:
            username (str): The username of the user
            password (str): The password of the user
        """
        response = self._session.post(self.login_url, json={"username": username, "password": password})
        # TODO: do we want to do anything with the return value token in the future?
        verbose_raise_for_status(response)
        self._session.headers.update({"X-CSRFToken": self._session.cookies.get("csrftoken")})

    def get(self, resource: str, **kwargs) -> requests.Response:
        """Make a get request to the Doccano API

        Args:
            resource (str): The resource to get
            kwargs: Additional arguments to pass to the request

        Returns:
            requests.Response: The response from the API
        """
        if resource.startswith(self.api_url):
            resource = resource[len(self.api_url) + 1 :]
        url = f"{self.api_url}/{resource}"
        response = self._session.get(url, **kwargs)
        verbose_raise_for_status(response)
        return response

    def post(self, resource: str, **kwargs) -> requests.Response:
        """Make a post request to the Doccano API

        Args:
            resource (str): The resource to post
            kwargs: Additional arguments to pass to the request

        Returns:
            requests.Response: The response from the API
        """
        url = f"{self.api_url}/{resource}"
        response = self._session.post(url, **kwargs)
        verbose_raise_for_status(response)
        return response

    def put(self, resource: str, **kwargs) -> requests.Response:
        """Make a put request to the Doccano API

        Args:
            resource (str): The resource to put
            kwargs: Additional arguments to pass to the request

        Returns:
            requests.Response: The response from the API
        """
        url = f"{self.api_url}/{resource}"
        response = self._session.put(url, **kwargs)
        verbose_raise_for_status(response)
        return response

    def delete(self, resource: str, **kwargs) -> requests.Response:
        """Make a delete request to the Doccano API

        Args:
            resource (str): The resource to delete
            kwargs: Additional arguments to pass to the request

        Returns:
            requests.Response: The response from the API
        """
        url = f"{self.api_url}/{resource}"
        response = self._session.delete(url, **kwargs)
        verbose_raise_for_status(response)
        return response
