import pytest

from doccano_client.repositories.base import get_next_url


@pytest.mark.parametrize(
    "base_url,initial_request_url,response_url,next_url",
    [
        (
            "https://hostname.ca",
            "https://hostname.ca/projects",
            "http://hostname.ca/projects?limit=5&offset=5",
            "https://hostname.ca/projects?limit=5&offset=5",
        ),
        (
            "https://hostname.ca",
            "https://hostname.ca/projects",
            "http://localhost:3000/projects?limit=5&offset=5",
            "https://hostname.ca/projects?limit=5&offset=5",
        ),
        (
            "https://hostname.ca",
            "https://hostname.ca/projects",
            "http://localhost:3000/projects?limit=5&offset=5",
            "https://hostname.ca/projects?limit=5&offset=5",
        ),
        (
            "https://hostname.ca",
            "https://hostname.ca/projects",
            "https://hostname.ca/projects?limit=5&offset=5",
            "https://hostname.ca/projects?limit=5&offset=5",
        ),
    ],
)
def test_get_next_url(base_url, initial_request_url, response_url, next_url):
    url = get_next_url(base_url, initial_request_url, {"next": response_url})
    assert url == next_url


@pytest.mark.parametrize(
    "base_url,initial_request_url,response_url",
    [
        (
            "https://hostname.ca",
            "https://hostname.ca/projects",
            "http://hostname.ca/things?limit=5&offset=5",
        ),
    ],
)
def test_get_next_url_error(base_url, initial_request_url, response_url):
    # should return the unmodified url when in doubt
    url = get_next_url(base_url, initial_request_url, {"next": response_url})
    assert url == response_url
