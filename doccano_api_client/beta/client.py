import requests

from .controllers import ProjectsController
from .utils.response import verbose_raise_for_status


class DoccanoClient:
    """Base client for interacting with the Doccano API"""

    __slots__ = ["_base_url", "client_session"]

    def __init__(self, base_url: str) -> None:
        """Initialize a Doccano client with a base url and authorization token for headers"""
        self._base_url = base_url
        self.client_session = requests.Session()
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "referer": base_url,
        }
        self.client_session.headers.update(headers)

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
        response = self.client_session.post(self.login_url, json={"username": username, "password": password})
        # TODO: do we want to do anything with the return value token in the future?
        verbose_raise_for_status(response)
        self.client_session.headers.update({"X-CSRFToken": self.client_session.cookies.get("csrftoken")})

    @property
    def projects(self) -> ProjectsController:
        """Return a generated project controller based on api url and client session"""
        return ProjectsController(self.api_url, self.client_session)
