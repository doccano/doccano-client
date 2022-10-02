import requests

from .beta.utils.response import verbose_raise_for_status


class DoccanoClient:
    """Base client for interacting with the Doccano API"""

    __slots__ = ["_base_url", "session"]

    def __init__(self, base_url: str) -> None:
        """Initialize a Doccano client with a base url and authorization token for headers"""
        self._base_url = base_url
        self.session = requests.Session()
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "referer": base_url,
        }
        self.session.headers.update(headers)

    @property
    def login_url(self) -> str:
        """Retrieve an API login url based on the base_url"""
        return f"{self._base_url}/v1/auth/login/"

    @property
    def api_url(self) -> str:
        """Retrieve an API url based on the base_url"""
        return f"{self._base_url}/v1"

    def login(self, username: str, password: str) -> None:
        """Login to a session with the Doccano instance related to the base url"""
        response = self.session.post(self.login_url, json={"username": username, "password": password})
        # TODO: do we want to do anything with the return value token in the future?
        verbose_raise_for_status(response)
        self.session.headers.update({"X-CSRFToken": self.session.cookies.get("csrftoken")})

    def get(self, resource: str, **kwargs) -> requests.Response:
        """Make a get request to the Doccano API"""
        url = f"{self.api_url}/{resource}"
        response = self.session.get(url, **kwargs)
        verbose_raise_for_status(response)
        return response

    def post(self, resource: str, **kwargs) -> requests.Response:
        """Make a post request to the Doccano API"""
        url = f"{self.api_url}/{resource}"
        response = self.session.post(url, **kwargs)
        verbose_raise_for_status(response)
        return response

    def put(self, resource: str, **kwargs) -> requests.Response:
        """Make a put request to the Doccano API"""
        url = f"{self.api_url}/{resource}"
        response = self.session.put(url, **kwargs)
        verbose_raise_for_status(response)
        return response

    def delete(self, resource: str, **kwargs) -> requests.Response:
        """Make a delete request to the Doccano API"""
        url = f"{self.api_url}/{resource}"
        response = self.session.delete(url, **kwargs)
        verbose_raise_for_status(response)
        return response
