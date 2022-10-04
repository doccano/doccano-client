from unittest import TestCase

import responses
from requests import Session

from ...controllers import CategoriesController
from ...models import Project, ProjectTypes
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import categories as mocks


class CategoriesControllerTest(TestCase):
    def setUp(self) -> None:
        self.project = Project(
            name="my_project",
            description="Project description",
            project_type=ProjectTypes.DOCUMENT_CLASSIFICATION,
        )

        self.categories_controller = CategoriesController(
            example_id=123,
            project=self.project,
            example_url="http://api/v1/projects/123/examples/123",
            client_session=Session(),
        )

    @responses.activate
    def test_all(self) -> None:
        responses.add(mocks.categories_get_response)
        category_controllers = list(self.categories_controller.all())

        expected_categories_id_map = {category_json["id"]: category_json for category_json in mocks.categories_get_json}

        for category_controller in category_controllers:
            category_id = category_controller.id
            category = category_controller.category
            self.assertIn(category_id, expected_categories_id_map)
            self.assertEqual(category.label, expected_categories_id_map[category_id]["label"])
            self.assertEqual(category.prob, expected_categories_id_map[category_id]["prob"])

        self.assertEqual(len(category_controllers), len(mocks.categories_get_json))

    @responses.activate
    def test_all_with_bad_response(self) -> None:
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.categories_controller.all())
