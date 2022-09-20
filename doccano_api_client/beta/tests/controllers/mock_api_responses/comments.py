import re

import responses

from . import projects

comments_get_json = [
    {
        "id": 109,
        "user": 1,
        "username": "mock_user",
        "example": 11,
        "text": "You thought it was a comment text, but it was me, Dio!",
        "created_at": "2021-07-23T17:29:21.797607Z",
    },
    {
        "id": 108,
        "user": 1,
        "username": "mock_user",
        "example": 11,
        "text": "General Kenobi",
        "created_at": "2021-07-23T17:29:14.890131Z",
    },
]

comments_regex = rf".*/v1/projects/{projects.valid_project_ids_regex_insert}/(examples/\d+/)*comments"

comments_get_empty_response = responses.Response(method="GET", url=re.compile(comments_regex), json=[], status=200)

comments_get_response = responses.Response(
    method="GET", url=re.compile(comments_regex), json=comments_get_json, status=200
)
