import pathlib

import requests
from requests_toolbelt import MultipartEncoder

from .beta.utils.response import verbose_raise_for_status


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

    def get(self, resource: str, **kwargs) -> requests.Response:
        """Make a get request to the Doccano API"""
        url = f"{self.api_url}/{resource}"
        response = self.client_session.get(url, params=kwargs)
        verbose_raise_for_status(response)
        return response

    def post(self, resource: str, **kwargs) -> requests.Response:
        """Make a post request to the Doccano API"""
        url = f"{self.api_url}/{resource}"
        response = self.client_session.post(url, json=kwargs)
        verbose_raise_for_status(response)
        return response

    def put(self, resource: str, **kwargs) -> requests.Response:
        """Make a put request to the Doccano API"""
        url = f"{self.api_url}/{resource}"
        response = self.client_session.put(url, json=kwargs)
        verbose_raise_for_status(response)
        return response

    def delete(self, resource: str, **kwargs) -> requests.Response:
        """Make a delete request to the Doccano API"""
        url = f"{self.api_url}/{resource}"
        response = self.client_session.delete(url, json=kwargs)
        verbose_raise_for_status(response)
        return response

    def upload(self, resource: str, file_path: str) -> requests.Response:
        """Upload a file to the Doccano API"""
        url = f"{self.api_url}/{resource}"
        file = pathlib.Path(file_path)
        with file.open("rb") as f:
            # headers = {
            #     "Content-Type": "multipart/form-data; boundary = something",
            # }
            # response = self.client_session.post(
            #     url, files={"file": (file.name, f, "application/json")}, headers=headers
            # )
            m = MultipartEncoder(fields={"file": (file.name, f, "application/json")})
            response = self.client_session.post(url, data=m, headers={"Content-Type": m.content_type})
        verbose_raise_for_status(response)
        return response
