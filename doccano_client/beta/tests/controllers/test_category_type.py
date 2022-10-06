from unittest import TestCase

import responses
from requests import Session

from ...controllers import CategoryTypeController, CategoryTypesController
from ...models import CategoryType
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import category_types as mocks


class CategoryTypeControllerTest(TestCase):
    def setUp(self):
        self.category_type_a = CategoryType(text="my text")
        self.category_type_controller_a = CategoryTypeController(
            category_type=self.category_type_a,
            id=43,
            category_types_url="http://my_category_types_url",
            client_session=Session(),
        )

    def test_urls(self):
        self.assertEqual(self.category_type_controller_a.category_type_url, "http://my_category_types_url/43")


class CategoryTypesControllerTest(TestCase):
    def setUp(self):
        self.category_type_a = CategoryType(text="next_test_label")
        self.category_type_controller_a = CategoryTypeController(
            category_type=self.category_type_a,
            id=43,
            category_types_url="http://my_category_types_url/v1/projects/23",
            client_session=Session(),
        )
        self.category_types_controller = CategoryTypesController("http://my_labels_url/v1/projects/23", Session())

    def test_controller_urls(self):
        self.assertEqual(
            self.category_types_controller.category_types_url, "http://my_labels_url/v1/projects/23/category-types"
        )

    @responses.activate
    def test_all_with_no_category_types(self):
        responses.add(mocks.category_types_get_empty_response)
        category_type_controllers = self.category_types_controller.all()
        self.assertEqual(len(list(category_type_controllers)), 0)

    @responses.activate
    def test_all(self):
        responses.add(mocks.category_types_get_response)
        category_type_controllers = self.category_types_controller.all()

        total_category_types = 0
        expected_category_type_id_dict = {
            category_type_json["id"]: category_type_json for category_type_json in mocks.category_types_get_json
        }
        for category_type_controller in category_type_controllers:
            self.assertIn(category_type_controller.id, expected_category_type_id_dict)
            self.assertEqual(
                category_type_controller.category_type.text,
                expected_category_type_id_dict[category_type_controller.id]["text"],
            )
            self.assertEqual(
                category_type_controller.category_type.suffix_key,
                expected_category_type_id_dict[category_type_controller.id]["suffix_key"],
            )
            self.assertIs(category_type_controller.client_session, self.category_types_controller.client_session)
            total_category_types += 1

        self.assertEqual(total_category_types, len(mocks.category_types_get_json))

    @responses.activate
    def test_all_with_bad_response(self):
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.category_types_controller.all())

    @responses.activate
    def test_create(self):
        responses.add(mocks.category_type_create_response)
        category_type_a_controller = self.category_types_controller.create(self.category_type_a)

        self.assertEqual(category_type_a_controller.id, mocks.category_type_create_json["id"])
        self.assertEqual(category_type_a_controller.category_type.text, mocks.category_type_create_json["text"])

    @responses.activate
    def test_create_with_bad_response(self):
        responses.add(bad.bad_post_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.category_types_controller.create(self.category_type_a))

    @responses.activate
    def test_update(self):
        responses.add(mocks.category_types_get_response)
        responses.add(mocks.category_type_update_response)
        category_type_controllers = self.category_types_controller.all()
        self.category_types_controller.update(category_type_controllers)

    @responses.activate
    def test_update_with_bad_response(self):
        responses.add(bad.bad_put_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.category_types_controller.update([self.category_type_controller_a]))
