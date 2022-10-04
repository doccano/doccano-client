from unittest import TestCase

import responses
from requests import Session

from ...controllers import RelationsController
from ...models import Project, ProjectTypes
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import relations as mocks


class RelationsControllerTest(TestCase):
    def setUp(self) -> None:
        self.project = Project(
            name="my_project",
            description="Project description",
            project_type=ProjectTypes.SEQUENCE_LABELING,
        )

        self.relations_controller = RelationsController(
            example_id=123,
            project=self.project,
            example_url="http://api/v1/projects/123/examples/123",
            client_session=Session(),
        )

    @responses.activate
    def test_all(self) -> None:
        responses.add(mocks.relations_get_response)
        relation_controllers = list(self.relations_controller.all())

        expected_relations_id_map = {relation_json["id"]: relation_json for relation_json in mocks.relations_get_json}

        for relation_controller in relation_controllers:
            relation_id = relation_controller.id
            relation = relation_controller.relation
            self.assertIn(relation_id, expected_relations_id_map)
            self.assertEqual(relation.type, expected_relations_id_map[relation_id]["type"])
            self.assertEqual(relation.prob, expected_relations_id_map[relation_id]["prob"])

        self.assertEqual(len(relation_controllers), len(mocks.relations_get_json))

    @responses.activate
    def test_all_with_bad_response(self) -> None:
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.relations_controller.all())
