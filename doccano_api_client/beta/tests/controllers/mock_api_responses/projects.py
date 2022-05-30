import re

import responses

projects_get_json = [
    {
        "id": 2,
        "name": "somethingsomething2",
        "description": "test 2",
        "guideline": "Please write annotation guideline.",
        "users": [1],
        "current_users_role": {
            "is_project_admin": True,
            "is_annotator": False,
            "is_annotation_approver": False,
        },
        "project_type": "SequenceLabeling",
        "updated_at": "2021-02-16T16:26:52.395900Z",
        "random_order": False,
        "collaborative_annotation": False,
        "single_class_classification": False,
        "resourcetype": "SequenceLabelingProject",
    },
    {
        "id": 4,
        "name": "DoesHTMLWork",
        "description": "Does it?",
        "guideline": "Please write annotation guideline.",
        "users": [1],
        "current_users_role": {
            "is_project_admin": True,
            "is_annotator": False,
            "is_annotation_approver": False,
        },
        "project_type": "Seq2seq",
        "updated_at": "2021-02-18T20:55:17.148231Z",
        "random_order": False,
        "collaborative_annotation": False,
        "single_class_classification": False,
        "resourcetype": "Seq2seqProject",
    },
    {
        "id": 3,
        "name": "somethingsomething3",
        "description": "test 3",
        "guideline": "Please write annotation guideline.",
        "users": [1],
        "current_users_role": {
            "is_project_admin": True,
            "is_annotator": False,
            "is_annotation_approver": False,
        },
        "project_type": "Seq2seq",
        "updated_at": "2021-02-22T17:18:26.942433Z",
        "random_order": True,
        "collaborative_annotation": False,
        "single_class_classification": False,
        "resourcetype": "Seq2seqProject",
    },
    {
        "id": 5,
        "name": "DoesHTMLWork2",
        "description": "Hithere",
        "guideline": "Please write annotation guideline.",
        "users": [1],
        "current_users_role": {
            "is_project_admin": True,
            "is_annotator": False,
            "is_annotation_approver": False,
        },
        "project_type": "Seq2seq",
        "updated_at": "2021-02-26T15:21:09.097168Z",
        "random_order": False,
        "collaborative_annotation": False,
        "single_class_classification": False,
        "resourcetype": "Seq2seqProject",
    },
    {
        "id": 1,
        "name": "somethingsomething",
        "description": "test 1",
        "guideline": "Please write annotation guideline.",
        "users": [1],
        "current_users_role": {
            "is_project_admin": True,
            "is_annotator": False,
            "is_annotation_approver": False,
        },
        "project_type": "DocumentClassification",
        "updated_at": "2021-03-10T22:07:35.323946Z",
        "random_order": False,
        "collaborative_annotation": False,
        "single_class_classification": False,
        "resourcetype": "TextClassificationProject",
    },
    {
        "id": 21,
        "name": "Test Admin 1",
        "description": "Test Admin 1",
        "guideline": "Please write annotation guideline.",
        "users": [1],
        "current_users_role": {
            "is_project_admin": True,
            "is_annotator": False,
            "is_annotation_approver": False,
        },
        "project_type": "DocumentClassification",
        "updated_at": "2021-03-23T07:01:50.729801Z",
        "random_order": False,
        "collaborative_annotation": False,
        "single_class_classification": False,
        "resourcetype": "TextClassificationProject",
    },
    {
        "id": 22,
        "name": "Test Admin 2",
        "description": "something",
        "guideline": "Please write annotation guideline.",
        "users": [1],
        "current_users_role": {
            "is_project_admin": True,
            "is_annotator": False,
            "is_annotation_approver": False,
        },
        "project_type": "DocumentClassification",
        "updated_at": "2021-03-23T15:05:42.133855Z",
        "random_order": False,
        "collaborative_annotation": False,
        "single_class_classification": False,
        "resourcetype": "TextClassificationProject",
    },
    {
        "id": 23,
        "name": "Test Admin 3",
        "description": "test",
        "guideline": "Please write annotation guideline.",
        "users": [1],
        "current_users_role": {
            "is_project_admin": True,
            "is_annotator": False,
            "is_annotation_approver": False,
        },
        "project_type": "DocumentClassification",
        "updated_at": "2021-03-23T15:09:00.433330Z",
        "random_order": False,
        "collaborative_annotation": False,
        "single_class_classification": False,
        "resourcetype": "TextClassificationProject",
    },
    {
        "id": 24,
        "name": "Test Admin 4",
        "description": "test",
        "guideline": "Please write annotation guideline.",
        "users": [1],
        "current_users_role": {
            "is_project_admin": True,
            "is_annotator": False,
            "is_annotation_approver": False,
        },
        "project_type": "Seq2seq",
        "updated_at": "2021-03-23T15:20:51.971295Z",
        "random_order": False,
        "collaborative_annotation": False,
        "single_class_classification": False,
        "resourcetype": "Seq2seqProject",
    },
]

project_create_json = {
    "id": 26,
    "name": "new client project",
    "description": "we da best",
    "guideline": "this kong has a funny face",
    "users": [1],
    "current_users_role": {
        "is_project_admin": True,
        "is_annotator": False,
        "is_annotation_approver": False,
    },
    "project_type": "SequenceLabeling",
    "updated_at": "2021-06-03T18:30:16.116377Z",
    "random_order": False,
    "collaborative_annotation": False,
    "single_class_classification": False,
    "resourcetype": "SequenceLabelingProject",
}

project_get_json = {
    "id": 24,
    "name": "Test Admin 4",
    "description": "test",
    "guideline": "Please write annotation guideline.",
    "users": [1],
    "current_users_role": {
        "is_project_admin": True,
        "is_annotator": False,
        "is_annotation_approver": False,
    },
    "project_type": "Seq2seq",
    "updated_at": "2021-03-23T15:20:51.971295Z",
    "random_order": False,
    "collaborative_annotation": False,
    "single_class_classification": False,
    "resourcetype": "Seq2seqProject",
}

# Used for creating the labels and examples valid mock urls in their respective modules
valid_project_ids_regex_insert = (
    "(" + "|".join([str(project["id"]) for project in projects_get_json]) + ")"
)

projects_get_empty_response = responses.Response(
    method="GET", url=re.compile(".*/v1/projects"), json=[], status=200
)

projects_get_response = responses.Response(
    method="GET", url=re.compile(".*/v1/projects"), json=projects_get_json, status=200
)

project_get_response = responses.Response(
    method="GET",
    url=re.compile(f".*/v1/projects/{project_get_json['id']}"),
    json=project_get_json,
    status=200,
)

project_create_response = responses.Response(
    method="POST", url=re.compile(".*/v1/projects"), json=project_create_json, status=201
)
