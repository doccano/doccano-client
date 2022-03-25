import re

import responses

from . import projects

examples_get_json = {
    "count": 6,
    "next": "fake_next_url_should_not_be_used",
    "previous": None,
    "results": [
        {
            "id": 4,
            "text": "Sentiment Analysis is pretty cool",
            "annotations": [],
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
        },
        {
            "id": 5,
            "text": "Sentiment Analysis is meh",
            "annotations": [],
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
        },
        {
            "id": 6,
            "text": "Sentiment Analysis is neat?",
            "annotations": [],
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
        },
    ],
}

examples_get_json_second_page = {
    "count": 6,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": 7,
            "text": "Sentiment Analysis is pretty cool",
            "annotations": [],
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
        },
        {
            "id": 8,
            "text": "Sentiment Analysis is meh",
            "annotations": [],
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
        },
        {
            "id": 9,
            "text": "Sentiment Analysis is neat?",
            "annotations": [],
            "meta": {},
            "annotation_approver": None,
            "comment_count": 0,
        },
    ],
}

example_create_json = {
    "id": 49,
    "text": "This is an example text2",
    "annotations": [],
    "meta": {"key": "val"},
    "annotation_approver": None,
    "comment_count": 0,
}

example_get_json = {
    "id": 9,
    "text": "Sentiment Analysis is neat?",
    "annotations": [],
    "meta": {},
    "annotation_approver": None,
    "comment_count": 0,
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
