from unittest import TestCase

import pytest

from ..client import DoccanoClient
from ..models import Example, Label, Project

DOCCANO_ENDPOINT = "http://localhost:8000"  # TODO: Make this a pytest parameter or ENV variable
DOCCANO_USER = "admin"  # TODO: Make this a pytest parameter or ENV variable
DOCCANO_PASS = "password"  # TODO: Make this a pytest parameter or ENV variable


@pytest.mark.localintegrationtest
class IntegrationTests(TestCase):
    """Only works if Doccano is spinned up locally and accessible at 0.0.0.0

    Goal is to test integration of the client fully with the Doccano project,
    for instance in case of API breaking changes."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = DoccanoClient(DOCCANO_ENDPOINT)
        cls.client.login(DOCCANO_USER, DOCCANO_PASS)
        cls.projects_controller = cls.client.projects

        # Create a project
        cls.project = Project(
            name="Test Project",
            description="Test project",
            project_type="SequenceLabeling",
        )
        cls.project_controller = cls.client.projects.create(cls.project)
        cls.new_project_id = cls.project_controller.id

        # Create a example and associate it with the project
        cls.example = Example(text="Netflix and Amazon are both big tech companies.")
        cls.examples_controller = cls.project_controller.examples

        cls.example_controller = cls.examples_controller.create(cls.example)
        cls.new_example_id = cls.example_controller.id

        cls.label = Label(text="company")
        cls.label_controller = cls.project_controller.labels.create(cls.label)

        # Generate a comment for the example.
        # Currently, we do not have a CommentsController.create method, which is
        # by design. For the sake of integration test simulations, however,
        # we can still use the API to manually create them.
        cls.example_controller.client_session.post(
            cls.example_controller.comments.comments_url, json={"text": "hi there i'm a comment"}
        )

    @classmethod
    def tearDownClass(cls):
        cls.project_controller.client_session.delete(cls.project_controller.project_url)

    def test_project_got_created(self) -> None:
        project_controllers = self.projects_controller.all()
        self.assertNotEqual(len(list(project_controllers)), 0)

    def test_projects_controller_get(self) -> None:
        # Id should be 1 since it's the only project
        project_controller = self.projects_controller.get(self.new_project_id)
        self.assertEqual(project_controller, self.project_controller)

    def test_examples_comments_annotations_controllers(self) -> None:
        examples = self.examples_controller.all()
        self.assertEqual(len(list(examples)), 1)
        n_examples = self.examples_controller.count()
        self.assertEqual(n_examples, 1)
        example = self.examples_controller.get(self.new_example_id)

        example_with_expected_comments = self.example
        example_with_expected_comments.comment_count = 1

        self.assertEqual(example.example, self.example)

        comments_controller = example.comments
        comments = list(comments_controller.all())
        self.assertEqual(comments[0].comment.text, "hi there i'm a comment")

        # TODO: Right now, we can't create annotations intuitively in the API. Doccano v1.6.0
        #       should once it's released. Add annotations creation to integration tests and
        #       test structure so that we're exhaustively checking that endpoint.
        annotations_controller = example.annotations
        annotations = list(annotations_controller.all())
        self.assertEqual(len(annotations), 0)

    def test_labels_controller(self) -> None:
        expected_label = Label(text="company")
        label_controllers = list(self.project_controller.labels.all())
        self.assertEqual(expected_label, label_controllers[0].label)
