from __future__ import annotations

from typing import Optional

import requests
from requests import Response, exceptions

from doccano_client.exceptions import DoccanoAPIError


def get_next_url(base_url: str, initial_url: str, response_data: dict) -> Optional[str]:
    """
    Get the "next" url from the response object correcting for issues when the API is running
    at the non-default ports

    Args:
        base_url: the base url of the doccano instance which is passed when creating the doccano client
        initial_url: the url which was used for the first non-paged request
        response_data: the json payload from the reponse

    Returns:
        The adjusted url to get the next page or None when no next page is available

    """
    if response_data.get("next") is None:
        return None
    next_url = response_data["next"]
    try:
        resource = initial_url[len(base_url) :]
        _, next_suffix = next_url.split(resource)
        return base_url + resource + next_suffix
    except ValueError:
        # fallback to returning the unmodified next url
        return next_url


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
        raise DoccanoAPIError(str(err), err.response)
    return response


class BaseRepository:
    """Base repository for interacting with the Doccano API"""

    def __init__(self, base_url: str, verify: Optional[str | bool] = None) -> None:
        """Initialize the repository with the base url

        Args:
            base_url (str): The base url of the Doccano instance
            verify (str | bool): Either a boolean, in which case it controls whether we verify
                the server's TLS certificate, or a string, in which case it must be a path
                to a CA bundle to use. Defaults to ``True``. When set to
                ``False``, requests will accept any TLS certificate presented by
                the server, and will ignore hostname mismatches and/or expired
                certificates, which will make your application vulnerable to
                man-in-the-middle (MitM) attacks. Setting verify to ``False``
                may be useful during local development or testing.
        """
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        if verify is not None:
            self._session.verify = verify
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
        return f"{self.api_url}/auth/login/"

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

    def logout(self) -> None:
        """Logout of the session"""
        url = f"{self.api_url}/auth/logout/"
        response = self._session.post(url)
        verbose_raise_for_status(response)
        self._session.close()

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
