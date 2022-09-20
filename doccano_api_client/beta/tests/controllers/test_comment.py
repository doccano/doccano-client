from unittest import TestCase

import responses
from requests import Session

from ...controllers import CommentController, CommentsController
from ...models import Comment
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import comments as mocks


class CommentControllerTest(TestCase):
    def setUp(self):
        self.comment_a = Comment(text="my text")
        self.comment_controller_a = CommentController(
            comment=self.comment_a,
            id=43,
            username="kenobi",
            created_at="sometimestamp",
            example=11,
            comments_url="http://my_comments_url",
            client_session=Session(),
        )

    def test_urls(self):
        self.assertEqual(self.comment_controller_a.comment_url, "http://my_comments_url/43")


class CommentsControllerTest(TestCase):
    def setUp(self):
        self.comments_controller_from_example = CommentsController(
            "http://my_comments_url/v1/projects/23/examples/11", Session()
        )
        self.comments_controller_from_project = CommentsController("http://my_comments_url/v1/projects/23", Session())

    def test_controller_urls(self):
        self.assertEqual(
            self.comments_controller_from_example.comments_url,
            "http://my_comments_url/v1/projects/23/examples/11/comments",
        )
        self.assertEqual(
            self.comments_controller_from_project.comments_url,
            "http://my_comments_url/v1/projects/23/comments",
        )

    @responses.activate
    def test_all_with_no_comments_from_example(self):
        responses.add(mocks.comments_get_empty_response)
        comment_controllers = self.comments_controller_from_example.all()
        self.assertEqual(len(list(comment_controllers)), 0)

    @responses.activate
    def test_all_with_no_comments_from_project(self):
        responses.add(mocks.comments_get_empty_response)
        comment_controllers = self.comments_controller_from_project.all()
        self.assertEqual(len(list(comment_controllers)), 0)

    @responses.activate
    def test_all_from_example(self):
        responses.add(mocks.comments_get_response)
        comment_controllers = self.comments_controller_from_example.all()

        total_comments = 0
        expected_comment_id_dict = {comment_json["id"]: comment_json for comment_json in mocks.comments_get_json}
        for comment_controller in comment_controllers:
            self.assertIn(comment_controller.id, expected_comment_id_dict)
            self.assertEqual(
                comment_controller.comment.text,
                expected_comment_id_dict[comment_controller.id]["text"],
            )
            self.assertIs(
                comment_controller.client_session,
                self.comments_controller_from_example.client_session,
            )
            total_comments += 1

        self.assertEqual(total_comments, len(mocks.comments_get_json))

    @responses.activate
    def test_all_from_project(self):
        responses.add(mocks.comments_get_response)
        comment_controllers = self.comments_controller_from_project.all()

        total_comments = 0
        expected_comment_id_dict = {comment_json["id"]: comment_json for comment_json in mocks.comments_get_json}
        for comment_controller in comment_controllers:
            self.assertIn(comment_controller.id, expected_comment_id_dict)
            self.assertEqual(
                comment_controller.comment.text,
                expected_comment_id_dict[comment_controller.id]["text"],
            )
            self.assertIs(
                comment_controller.client_session,
                self.comments_controller_from_project.client_session,
            )
            total_comments += 1

        self.assertEqual(total_comments, len(mocks.comments_get_json))

    @responses.activate
    def test_all_with_bad_response(self):
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.comments_controller_from_example.all())

        with self.assertRaises(DoccanoAPIError):
            list(self.comments_controller_from_project.all())
