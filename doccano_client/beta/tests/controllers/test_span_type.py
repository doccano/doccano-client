from unittest import TestCase

import responses
from requests import Session

from ...controllers import SpanTypeController, SpanTypesController
from ...models import SpanType
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import span_types as mocks


class SpanTypeControllerTest(TestCase):
    def setUp(self):
        self.span_type_a = SpanType(text="my text")
        self.span_type_controller_a = SpanTypeController(
            span_type=self.span_type_a, id=43, span_types_url="http://my_span_types_url", client_session=Session()
        )

    def test_urls(self):
        self.assertEqual(self.span_type_controller_a.span_type_url, "http://my_span_types_url/43")


class SpanTypesControllerTest(TestCase):
    def setUp(self):
        self.span_type_a = SpanType(text="next_test_label")
        self.span_type_controller_a = SpanTypeController(
            span_type=self.span_type_a,
            id=43,
            span_types_url="http://my_span_types_url/v1/projects/23",
            client_session=Session(),
        )
        self.span_types_controller = SpanTypesController("http://my_labels_url/v1/projects/23", Session())

    def test_controller_urls(self):
        self.assertEqual(self.span_types_controller.span_types_url, "http://my_labels_url/v1/projects/23/span-types")

    @responses.activate
    def test_all_with_no_span_types(self):
        responses.add(mocks.span_types_get_empty_response)
        span_type_controllers = self.span_types_controller.all()
        self.assertEqual(len(list(span_type_controllers)), 0)

    @responses.activate
    def test_all(self):
        responses.add(mocks.span_types_get_response)
        span_type_controllers = self.span_types_controller.all()

        total_span_types = 0
        expected_span_type_id_dict = {
            span_type_json["id"]: span_type_json for span_type_json in mocks.span_types_get_json
        }
        for span_type_controller in span_type_controllers:
            self.assertIn(span_type_controller.id, expected_span_type_id_dict)
            self.assertEqual(
                span_type_controller.span_type.text, expected_span_type_id_dict[span_type_controller.id]["text"]
            )
            self.assertEqual(
                span_type_controller.span_type.suffix_key,
                expected_span_type_id_dict[span_type_controller.id]["suffix_key"],
            )
            self.assertIs(span_type_controller.client_session, self.span_types_controller.client_session)
            total_span_types += 1

        self.assertEqual(total_span_types, len(mocks.span_types_get_json))

    @responses.activate
    def test_all_with_bad_response(self):
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.span_types_controller.all())

    @responses.activate
    def test_create(self):
        responses.add(mocks.span_type_create_response)
        span_type_a_controller = self.span_types_controller.create(self.span_type_a)

        self.assertEqual(span_type_a_controller.id, mocks.span_type_create_json["id"])
        self.assertEqual(span_type_a_controller.span_type.text, mocks.span_type_create_json["text"])

    @responses.activate
    def test_create_with_bad_response(self):
        responses.add(bad.bad_post_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.span_types_controller.create(self.span_type_a))

    @responses.activate
    def test_update(self):
        responses.add(mocks.span_types_get_response)
        responses.add(mocks.span_type_update_response)
        span_type_controllers = self.span_types_controller.all()
        self.span_types_controller.update(span_type_controllers)

    @responses.activate
    def test_update_with_bad_response(self):
        responses.add(bad.bad_put_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.span_types_controller.update([self.span_type_controller_a]))
