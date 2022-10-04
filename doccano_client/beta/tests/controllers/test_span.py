from unittest import TestCase

import responses
from requests import Session

from ...controllers import SpansController
from ...models import Project, ProjectTypes
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import spans as mocks


class SpansControllerTest(TestCase):
    def setUp(self) -> None:
        self.project = Project(
            name="my_project",
            description="Project description",
            project_type=ProjectTypes.SEQUENCE_LABELING,
        )

        self.spans_controller = SpansController(
            example_id=123,
            project=self.project,
            example_url="http://api/v1/projects/123/examples/123",
            client_session=Session(),
        )

    @responses.activate
    def test_all(self) -> None:
        responses.add(mocks.spans_get_response)
        span_controllers = list(self.spans_controller.all())

        expected_spans_id_map = {span_json["id"]: span_json for span_json in mocks.spans_get_json}

        for span_controller in span_controllers:
            span_id = span_controller.id
            span = span_controller.span
            self.assertIn(span_id, expected_spans_id_map)
            self.assertEqual(span.label, expected_spans_id_map[span_id]["label"])
            self.assertEqual(span.prob, expected_spans_id_map[span_id]["prob"])

        self.assertEqual(len(span_controllers), len(mocks.spans_get_json))

    @responses.activate
    def test_all_with_bad_response(self) -> None:
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.spans_controller.all())
