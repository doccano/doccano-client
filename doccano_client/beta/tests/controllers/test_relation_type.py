from unittest import TestCase

import responses
from requests import Session

from ...controllers import RelationTypeController, RelationTypesController
from ...models import RelationType
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import relation_types as mocks


class RelationTypeControllerTest(TestCase):
    def setUp(self):
        self.relation_type_a = RelationType(text="my text")
        self.relation_type_controller_a = RelationTypeController(
            relation_type=self.relation_type_a,
            id=43,
            relation_types_url="http://my_relation_types_url",
            client_session=Session(),
        )

    def test_urls(self):
        self.assertEqual(self.relation_type_controller_a.relation_type_url, "http://my_relation_types_url/43")


class RelationTypesControllerTest(TestCase):
    def setUp(self):
        self.relation_type_a = RelationType(text="next_test_label")
        self.relation_type_controller_a = RelationTypeController(
            relation_type=self.relation_type_a,
            id=43,
            relation_types_url="http://my_relation_types_url/v1/projects/23",
            client_session=Session(),
        )
        self.relation_types_controller = RelationTypesController("http://my_labels_url/v1/projects/23", Session())

    def test_controller_urls(self):
        self.assertEqual(
            self.relation_types_controller.relation_types_url, "http://my_labels_url/v1/projects/23/relation-types"
        )

    @responses.activate
    def test_all_with_no_relation_types(self):
        responses.add(mocks.relation_types_get_empty_response)
        relation_type_controllers = self.relation_types_controller.all()
        self.assertEqual(len(list(relation_type_controllers)), 0)

    @responses.activate
    def test_all(self):
        responses.add(mocks.relation_types_get_response)
        relation_type_controllers = self.relation_types_controller.all()

        total_relation_types = 0
        expected_relation_type_id_dict = {
            relation_type_json["id"]: relation_type_json for relation_type_json in mocks.relation_types_get_json
        }
        for relation_type_controller in relation_type_controllers:
            self.assertIn(relation_type_controller.id, expected_relation_type_id_dict)
            self.assertEqual(
                relation_type_controller.relation_type.text,
                expected_relation_type_id_dict[relation_type_controller.id]["text"],
            )
            self.assertEqual(
                relation_type_controller.relation_type.suffix_key,
                expected_relation_type_id_dict[relation_type_controller.id]["suffix_key"],
            )
            self.assertIs(relation_type_controller.client_session, self.relation_types_controller.client_session)
            total_relation_types += 1

        self.assertEqual(total_relation_types, len(mocks.relation_types_get_json))

    @responses.activate
    def test_all_with_bad_response(self):
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.relation_types_controller.all())

    @responses.activate
    def test_create(self):
        responses.add(mocks.relation_type_create_response)
        relation_type_a_controller = self.relation_types_controller.create(self.relation_type_a)

        self.assertEqual(relation_type_a_controller.id, mocks.relation_type_create_json["id"])
        self.assertEqual(relation_type_a_controller.relation_type.text, mocks.relation_type_create_json["text"])

    @responses.activate
    def test_create_with_bad_response(self):
        responses.add(bad.bad_post_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.relation_types_controller.create(self.relation_type_a))

    @responses.activate
    def test_update(self):
        responses.add(mocks.relation_types_get_response)
        responses.add(mocks.relation_type_update_response)
        relation_type_controllers = self.relation_types_controller.all()
        self.relation_types_controller.update(relation_type_controllers)

    @responses.activate
    def test_update_with_bad_response(self):
        responses.add(bad.bad_put_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.relation_types_controller.update([self.relation_type_controller_a]))
