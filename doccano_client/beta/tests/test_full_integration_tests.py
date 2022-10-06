from unittest import TestCase

import pytest

from ..client import DoccanoClient
from ..models import Example, Project, SpanType

DOCCANO_ENDPOINT = "http://localhost"  # TODO: Make this a pytest parameter or ENV variable
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

        cls.span_type = SpanType(text="company")
        cls.span_type_controller = cls.project_controller.span_types.create(cls.span_type)

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

    def test_examples_comments_spans_controllers(self) -> None:
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

        spans_controller = example.spans
        spans = list(spans_controller.all())
        self.assertEqual(len(spans), 0)

    def test_span_types_controller(self) -> None:
        expected_span_type = SpanType(text="company")
        span_type_controllers = list(self.project_controller.span_types.all())
        self.assertEqual(expected_span_type, span_type_controllers[0].span_type)
