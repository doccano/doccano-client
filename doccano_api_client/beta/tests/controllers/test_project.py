from unittest import TestCase

import responses
from requests import Session

from ...controllers import ProjectController, ProjectsController
from ...models import Project
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import projects as mocks


class ProjectControllerTest(TestCase):
    def setUp(self):
        self.project_a = Project(
            name=mocks.project_create_json["name"],
            description=mocks.project_create_json["description"],
            project_type=mocks.project_create_json["project_type"],
        )
        self.project_controller_a = ProjectController(
            project=self.project_a,
            id=42,
            projects_url="http://my_projects_url",
            client_session=Session(),
        )

    def test_rejects_improper_project_type(self):
        with self.assertRaises(AssertionError):
            Project(
                name=mocks.project_create_json["name"],
                description=mocks.project_create_json["description"],
                project_type="bad_project_type",
            )

    def test_urls(self):
        self.assertEqual(self.project_controller_a.project_url, "http://my_projects_url/42")

    def test_labels(self):
        labels = self.project_controller_a.labels

        # Disable protected-access check for test case
        self.assertEqual(
            labels._project_url,  # pylint: disable=protected-access
            self.project_controller_a.project_url,
        )
        self.assertIs(labels.client_session, self.project_controller_a.client_session)

    def test_examples(self):
        examples = self.project_controller_a.examples

        # Disable protected-access check for test case
        self.assertEqual(
            examples._project_url,  # pylint: disable=protected-access
            self.project_controller_a.project_url,
        )
        self.assertIs(examples.client_session, self.project_controller_a.client_session)


class ProjectsControllerTest(TestCase):
    def setUp(self):
        self.project_a = Project(
            name=mocks.project_create_json["name"],
            description=mocks.project_create_json["description"],
            project_type=mocks.project_create_json["project_type"],
        )
        self.projects_controller = ProjectsController("http://my_api_url/v1", Session())

    def test_controller_urls(self):
        self.assertEqual(self.projects_controller.projects_url, "http://my_api_url/v1/projects")

    @responses.activate
    def test_all_with_no_projects(self):
        responses.add(mocks.projects_get_empty_response)
        project_controllers = self.projects_controller.all()
        self.assertEqual(len(list(project_controllers)), 0)

    @responses.activate
    def test_all(self):
        responses.add(mocks.projects_get_response)
        project_controllers = self.projects_controller.all()

        total_projects = 0
        expected_project_id_dict = {proj_json["id"]: proj_json for proj_json in mocks.projects_get_json["results"]}
        for project_controller in project_controllers:
            self.assertIn(project_controller.id, expected_project_id_dict)
            self.assertEqual(
                project_controller.project.name,
                expected_project_id_dict[project_controller.id]["name"],
            )
            self.assertEqual(
                project_controller.project.description,
                expected_project_id_dict[project_controller.id]["description"],
            )
            self.assertIs(project_controller.client_session, self.projects_controller.client_session)
            total_projects += 1

        self.assertEqual(total_projects, len(mocks.projects_get_json["results"]))

    @responses.activate
    def test_all_with_bad_response(self):
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.projects_controller.all())

    @responses.activate
    def test_create(self):
        responses.add(mocks.project_create_response)
        project_a_controller = self.projects_controller.create(self.project_a)

        self.assertEqual(project_a_controller.id, mocks.project_create_json["id"])
        self.assertEqual(project_a_controller.project.name, mocks.project_create_json["name"])

    @responses.activate
    def test_create_with_bad_response(self):
        responses.add(bad.bad_post_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.projects_controller.create(self.project_a))

    @responses.activate
    def test_get(self) -> None:
        responses.add(mocks.project_get_response)

        project_id = mocks.project_get_json["id"]
        project_controller = self.projects_controller.get(project_id)

        self.assertEqual(project_controller.id, project_id)
        self.assertEqual(project_controller.project_url, f"http://my_api_url/v1/projects/{project_id}")
        self.assertEqual(project_controller.project.project_type, mocks.project_get_json["project_type"])
