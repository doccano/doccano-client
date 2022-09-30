import re

import responses

relations_get_json = [
    {
        "id": 1,
        "user": 1,
        "created_at": "2021-03-23T15:20:51.971295Z",
        "updated_at": "2021-03-23T15:20:51.971295Z",
        "example": 123,
        "type": 50,
        "prob": 0.2,
        "from_id": 5,
        "to_id": 10,
    },
    {
        "id": 2,
        "user": 1,
        "created_at": "2021-03-23T15:20:51.971295Z",
        "updated_at": "2021-03-23T15:20:51.971295Z",
        "example": 123,
        "type": 23,
        "prob": 0.0,
        "from_id": 10,
        "to_id": 15,
    },
]

relation_create_json = {
    "id": 2,
    "user": 1,
    "created_at": "2021-03-23T15:20:51.971295Z",
    "updated_at": "2021-03-23T15:20:51.971295Z",
    "example": 123,
    "type": 23,
    "prob": 0.0,
    "from_id": 5,
    "to_id": 15,
}


relations_get_response = responses.Response(
    method="GET",
    url=re.compile(r".*/v1/projects/\d+/examples/\d+/relations"),
    json=relations_get_json,
    status=200,
)

relation_create_response = responses.Response(
    method="POST",
    url=re.compile(r".*/v1/projects/\d+/examples/\d+/relations"),
    json=relation_create_json,
    status=201,
)
