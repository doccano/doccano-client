import re

import responses

texts_get_json = [
    {
        "id": 1,
        "user": 1,
        "created_at": "2021-03-23T15:20:51.971295Z",
        "updated_at": "2021-03-23T15:20:51.971295Z",
        "example": 123,
        "text": "lol",
        "prob": 0.2,
    },
    {
        "id": 2,
        "user": 1,
        "created_at": "2021-03-23T15:20:51.971295Z",
        "updated_at": "2021-03-23T15:20:51.971295Z",
        "example": 123,
        "text": "kek",
        "prob": 0.0,
    },
]

text_create_json = {
    "id": 2,
    "user": 1,
    "created_at": "2021-03-23T15:20:51.971295Z",
    "updated_at": "2021-03-23T15:20:51.971295Z",
    "example": 123,
    "text": "foo",
    "prob": 0.0,
}


texts_get_response = responses.Response(
    method="GET",
    url=re.compile(r".*/v1/projects/\d+/examples/\d+/texts"),
    json=texts_get_json,
    status=200,
)

text_create_response = responses.Response(
    method="POST",
    url=re.compile(r".*/v1/projects/\d+/examples/\d+/texts"),
    json=text_create_json,
    status=201,
)
