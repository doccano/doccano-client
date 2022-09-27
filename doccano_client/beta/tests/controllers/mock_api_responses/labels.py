import re

import responses

from . import projects

labels_get_json = [
    {
        "id": 6,
        "text": "test_label",
        "prefix_key": None,
        "suffix_key": "1",
        "background_color": "#2196F3",
        "text_color": "#ffffff",
    },
    {
        "id": 7,
        "text": "next_test_label",
        "prefix_key": None,
        "suffix_key": None,
        "background_color": "#2196F3",
        "text_color": "#ffffff",
    },
]

label_create_json = {
    "id": 7,
    "text": "next_test_label",
    "prefix_key": None,
    "suffix_key": None,
    "background_color": "#2196F3",
    "text_color": "#ffffff",
}

labels_regex = f".*/v1/projects/{projects.valid_project_ids_regex_insert}/labels"

labels_get_empty_response = responses.Response(method="GET", url=re.compile(labels_regex), json=[], status=200)

labels_get_response = responses.Response(method="GET", url=re.compile(labels_regex), json=labels_get_json, status=200)

label_create_response = projects_get_updated_response = responses.Response(
    method="POST",
    url=re.compile(labels_regex),
    json=label_create_json,
    status=201,
)

label_update_response = responses.Response(
    method="PUT",
    url=re.compile(rf"{labels_regex}/\d+"),
    # The json here in practice is way more complicated, but we don't need to test or use the
    # response outside of the status code, so it is moot for testing.
    json={"status": "accepted"},
    status=200,
)
