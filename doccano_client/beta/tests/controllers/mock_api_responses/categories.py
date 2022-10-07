import re

import responses

categories_get_json = [
    {
        "id": 1,
        "user": 1,
        "created_at": "2021-03-23T15:20:51.971295Z",
        "updated_at": "2021-03-23T15:20:51.971295Z",
        "example": 123,
        "label": 50,
        "prob": 0.2,
    },
    {
        "id": 2,
        "user": 1,
        "created_at": "2021-03-23T15:20:51.971295Z",
        "updated_at": "2021-03-23T15:20:51.971295Z",
        "example": 123,
        "label": 23,
        "prob": 0.0,
    },
]

category_create_json = {
    "id": 2,
    "user": 1,
    "created_at": "2021-03-23T15:20:51.971295Z",
    "updated_at": "2021-03-23T15:20:51.971295Z",
    "example": 123,
    "label": 23,
    "prob": 0.0,
}


categories_get_response = responses.Response(
    method="GET",
    url=re.compile(r".*/v1/projects/\d+/examples/\d+/categories"),
    json=categories_get_json,
    status=200,
)

category_create_response = responses.Response(
    method="POST",
    url=re.compile(r".*/v1/projects/\d+/examples/\d+/categories"),
    json=category_create_json,
    status=201,
)
