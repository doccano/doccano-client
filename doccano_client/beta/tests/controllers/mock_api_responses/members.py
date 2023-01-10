import re

import responses

from . import projects

members_get_json = [
    {
        "id": 6,
        "user": 1,
        "role": 1,
        "username": "user_a",
        "rolename": "project_admin",
    },
    {
        "id": 7,
        "user": 2,
        "role": 2,
        "username": "user_b",
        "rolename": "annotator",
    },
]

member_create_json = {
    "id": 8,
    "user": 3,
    "role": 3,
    "username": "user_c",
    "rolename": "annotation_approver",
}

members_regex = f".*/v1/projects/{projects.valid_project_ids_regex_insert}/members"

members_get_empty_response = responses.Response(method="GET", url=re.compile(members_regex), json=[], status=200)

members_get_response = responses.Response(
    method="GET", url=re.compile(members_regex), json=members_get_json, status=200
)

member_create_response = projects_get_updated_response = responses.Response(
    method="POST",
    url=re.compile(members_regex),
    json=member_create_json,
    status=201,
)

member_update_response = responses.Response(
    method="PUT",
    url=re.compile(rf"{members_regex}/\d+"),
    # The json here in practice is way more complicated, but we don't need to test or use the
    # response outside of the status code, so it is moot for testing.
    json={"status": "accepted"},
    status=200,
)
