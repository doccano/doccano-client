import re

import responses

from . import projects

examples_get_json = {
    "count": 6,
    "next": "https://doccano.xxxx.com/v1/projects/2/examples?confirmed=&limit=3&offset=3&q=",
    "previous": None,
    "results": [
        {
            "id": 4,
            "filename": "https://doccano.xxxx.com/media/",
            "text": "Sentiment Analysis is pretty cool",
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
            "is_confirmed": None,
            "upload_name": "",
        },
        {
            "id": 5,
            "filename": "https://doccano.xxxx.com/media/",
            "text": "Sentiment Analysis is meh",
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
            "is_confirmed": None,
            "upload_name": "",
        },
        {
            "id": 6,
            "filename": "https://doccano.xxxx.com/media/",
            "text": "Sentiment Analysis is neat?",
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
            "is_confirmed": None,
            "upload_name": "",
        },
    ],
}

examples_get_json_second_page = {
    "count": 6,
    "next": None,
    "previous": "https://doccano.xxxx.com/v1/projects/2/examples?confirmed=&limit=3&q=",
    "results": [
        {
            "id": 7,
            "filename": "https://doccano.xxxx.com/media/",
            "text": "Sentiment Analysis is pretty cool",
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
            "is_confirmed": None,
            "upload_name": "",
        },
        {
            "id": 8,
            "filename": "https://doccano.xxxx.com/media/",
            "text": "Sentiment Analysis is meh",
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
            "is_confirmed": None,
            "upload_name": "",
        },
        {
            "id": 9,
            "filename": "https://doccano.xxxx.com/media/",
            "text": "Sentiment Analysis is neat?",
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
            "is_confirmed": None,
            "upload_name": "",
        },
    ],
}

example_create_json = {
    "id": 49,
    "text": "This is an example text2",
    "meta": {"key": "val"},
    "annotation_approver": None,
    "comment_count": 0,
    "is_confirmed": True,
    "upload_name": "",
}

example_get_json = {
    "id": 9,
    "filename": "https://doccano.xxxx.com/media/",
    "text": "Sentiment Analysis is neat?",
    "meta": {},
    "annotation_approver": None,
    "comment_count": 0,
    "is_confirmed": True,
    "upload_name": "",
}

examples_regex = f".*/v1/projects/{projects.valid_project_ids_regex_insert}/examples"

examples_get_empty_response = responses.Response(
    method="GET",
    url=re.compile(examples_regex),
    json={"count": 0, "next": None, "results": []},
    status=200,
)

examples_get_response = responses.Response(
    method="GET", url=re.compile(examples_regex), json=examples_get_json, status=200
)

example_get_response = responses.Response(
    method="GET",
    url=re.compile(f"{examples_regex}/{example_get_json['id']}"),
    json=example_get_json,
    status=200,
)

examples_get_response_second_page = responses.Response(
    method="GET",
    url=re.compile(examples_regex + ".*?offset=.*"),
    json=examples_get_json_second_page,
    status=200,
)

example_create_response = projects_get_updated_response = responses.Response(
    method="POST", url=re.compile(examples_regex), json=example_create_json, status=201
)
