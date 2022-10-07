import re

import responses

from . import projects

category_types_get_json = [
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

category_type_create_json = {
    "id": 7,
    "text": "next_test_label",
    "prefix_key": None,
    "suffix_key": None,
    "background_color": "#2196F3",
    "text_color": "#ffffff",
}

category_types_regex = f".*/v1/projects/{projects.valid_project_ids_regex_insert}/category-types"

category_types_get_empty_response = responses.Response(
    method="GET", url=re.compile(category_types_regex), json=[], status=200
)

category_types_get_response = responses.Response(
    method="GET", url=re.compile(category_types_regex), json=category_types_get_json, status=200
)

category_type_create_response = projects_get_updated_response = responses.Response(
    method="POST",
    url=re.compile(category_types_regex),
    json=category_type_create_json,
    status=201,
)

category_type_update_response = responses.Response(
    method="PUT",
    url=re.compile(rf"{category_types_regex}/\d+"),
    # The json here in practice is way more complicated, but we don't need to test or use the
    # response outside of the status code, so it is moot for testing.
    json={"status": "accepted"},
    status=200,
)
