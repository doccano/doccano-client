from unittest import TestCase

import responses
from requests import Session

from ...controllers import ExampleController, ExamplesController
from ...models import CategoryAnnotation, Example, Project, ProjectTypes, SpanAnnotation
from ...utils.response import DoccanoAPIError
from .mock_api_responses import annotations as annotation_mocks
from .mock_api_responses import bad
from .mock_api_responses import examples as mocks


class ExampleControllerTest(TestCase):
    def setUp(self):
        project = Project(
            name="my-project",
            description="project description",
            project_type=ProjectTypes.DOCUMENT_CLASSIFICATION,
        )
        self.example_a = Example(text="my text")
        self.example_controller_a = ExampleController(
            project=project,
            example=self.example_a,
            id=43,
            examples_url="http://my_example_url",
            client_session=Session(),
        )

    def test_urls(self):
        self.assertEqual(self.example_controller_a.example_url, "http://my_example_url/43")


class ExamplesControllerTest(TestCase):
    def setUp(self):
        project = Project(
            name="my-project",
            description="project description",
            project_type=ProjectTypes.DOCUMENT_CLASSIFICATION,
        )
        self.example_a = Example(text="This is an example text2", meta={"key": "val"})
        self.examples_controller = ExamplesController(
            project, "http://my_examples_url/v1/projects/23", Session()
        )

    def test_controller_urls(self):
        self.assertEqual(
            self.examples_controller.examples_url, "http://my_examples_url/v1/projects/23/examples"
        )

    @responses.activate
    def test_rejects_incorrect_annotation_type(self) -> None:
        """Only annotations of the appropriate type should be allowed."""
        responses.add(bad.bad_post_response)
        with self.assertRaises(DoccanoAPIError):
            annotation = SpanAnnotation(label=1, prob=1.0, start_offset=0, end_offset=10)
            example = Example(text="blablabla", annotations=[annotation])
            self.examples_controller.create(example)

    @responses.activate
    def test_create_annotations(self) -> None:
        responses.add(annotation_mocks.annotation_create_response)
        responses.add(annotation_mocks.annotations_get_response)
        annotation = CategoryAnnotation(label=23, prob=0)
        example = Example(text="blablabla", annotations=[annotation])
        example_controller = self.examples_controller.create(example)

        # Client should choose the correct annotation serializer for creation given the project type
        self.assertTrue(
            isinstance(list(example_controller.annotations.all())[1].annotation, CategoryAnnotation)
        )

        # created_annotation = cast(CategoryAnnotation, annotation_controller.annotation)
        self.assertEqual(
            list(example_controller.annotations.all())[1].id,
            annotation_mocks.annotation_create_json["id"],
        )
        self.assertEqual(
            list(example_controller.annotations.all())[1].annotation.label,
            annotation_mocks.annotation_create_json["label"],
        )

    @responses.activate
    def test_create_annotations_with_bad_response(self) -> None:
        responses.add(bad.bad_post_response)
        with self.assertRaises(DoccanoAPIError):
            example = Example(text="blablabla", annotations=[CategoryAnnotation(label=1, prob=0)])
            self.examples_controller.create(example)

    @responses.activate
    def test_count_empty(self):
        responses.add(mocks.examples_get_empty_response)
        examples_count = self.examples_controller.count()
        self.assertEqual(examples_count, 0)

    @responses.activate
    def test_count_nonempty(self):
        responses.add(mocks.examples_get_response)
        examples_count = self.examples_controller.count()
        self.assertEqual(examples_count, 6)

    @responses.activate
    def test_all_with_no_examples(self):
        responses.add(mocks.examples_get_empty_response)
        example_controllers = self.examples_controller.all()
        self.assertEqual(len(list(example_controllers)), 0)

    @responses.activate
    def test_all(self):
        responses.add(mocks.examples_get_response)
        responses.add(mocks.examples_get_response_second_page)
        responses.add(mocks.examples_get_empty_response)
        example_controllers = self.examples_controller.all()

        total_examples = 0
        expected_example_id_dict = {
            example_json["id"]: example_json
            for example_json in mocks.examples_get_json["results"]
            + mocks.examples_get_json_second_page["results"]
        }
        for example_controller in example_controllers:
            self.assertIn(example_controller.id, expected_example_id_dict)
            self.assertEqual(
                example_controller.example.text,
                expected_example_id_dict[example_controller.id]["text"],
            )
            self.assertIs(
                example_controller.client_session, self.examples_controller.client_session
            )
            total_examples += 1

        self.assertEqual(
            total_examples,
            len(
                mocks.examples_get_json["results"] + mocks.examples_get_json_second_page["results"]
            ),
        )
        self.assertEqual(total_examples, mocks.examples_get_json["count"])

    @responses.activate
    def test_all_with_bad_response(self):
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.examples_controller.all())

    @responses.activate
    def test_create(self):
        responses.add(mocks.example_create_response)
        example_a_controller = self.examples_controller.create(self.example_a)

        self.assertEqual(example_a_controller.id, mocks.example_create_json["id"])
        self.assertEqual(example_a_controller.example.text, mocks.example_create_json["text"])
        self.assertEqual(example_a_controller.example.meta, {"key": "val"})

    @responses.activate
    def test_create_with_bad_response(self):
        responses.add(bad.bad_post_response)
        with self.assertRaises(DoccanoAPIError):
            self.examples_controller.create(self.example_a)

    @responses.activate
    def test_get(self) -> None:
        responses.add(mocks.example_get_response)

        example_id = mocks.example_get_json["id"]
        example_controller = self.examples_controller.get(example_id)

        self.assertEqual(example_controller.id, example_id)
        self.assertEqual(example_controller.project, self.examples_controller.project)
        self.assertEqual(example_controller.example.text, mocks.example_get_json["text"])
