from typing import cast
from unittest import TestCase

import responses
from requests import Session

from ...controllers import AnnotationsController
from ...models import CategoryAnnotation, Project, ProjectTypes
from ...utils.response import DoccanoAPIError
from .mock_api_responses import annotations as mocks
from .mock_api_responses import bad


class AnnotationsControllerTest(TestCase):
    def setUp(self) -> None:
        self.project = Project(
            name="my_project",
            description="Project description",
            project_type=ProjectTypes.DOCUMENT_CLASSIFICATION,
        )

        self.annotations_controller = AnnotationsController(
            example_id=123,
            project=self.project,
            example_url="http://api/v1/projects/123/examples/123",
            client_session=Session(),
        )

    @responses.activate
    def test_all(self) -> None:
        responses.add(mocks.annotations_get_response)
        annotation_controllers = list(self.annotations_controller.all())

        expected_annotations_id_map = {
            annotation_json["id"]: annotation_json for annotation_json in mocks.annotations_get_json["annotations"]
        }

        for annotation_controller in annotation_controllers:
            annotation_id = annotation_controller.id
            annotation = cast(CategoryAnnotation, annotation_controller.annotation)
            self.assertIn(annotation_id, expected_annotations_id_map)
            self.assertEqual(annotation.label, expected_annotations_id_map[annotation_id]["label"])
            self.assertEqual(annotation.prob, expected_annotations_id_map[annotation_id]["prob"])
            self.assertEqual(annotation_controller.user, expected_annotations_id_map[annotation_id]["user"])
            self.assertEqual(
                annotation_controller.created_at,
                expected_annotations_id_map[annotation_id]["created_at"],
            )
            self.assertEqual(
                annotation_controller.updated_at,
                expected_annotations_id_map[annotation_id]["updated_at"],
            )
            self.assertEqual(
                annotation_controller.example,
                expected_annotations_id_map[annotation_id]["example"],
            )

        self.assertEqual(len(annotation_controllers), len(mocks.annotations_get_json["annotations"]))

    @responses.activate
    def test_all_with_bad_response(self) -> None:
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.annotations_controller.all())
