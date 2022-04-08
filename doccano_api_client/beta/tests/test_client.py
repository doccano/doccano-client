import json
from unittest import TestCase

import responses

from ..client import DoccanoClient
from ..models import Example
from ..utils.response import DoccanoAPIError
from .controllers.mock_api_responses import examples as mock_examples
from .controllers.mock_api_responses import projects as mock_projects


class ClientTest(TestCase):
    def setUp(self):
        self.client = DoccanoClient("https://doccano.notaningress.com")

    def test_url_properties(self):
        self.assertEqual(self.client.login_url, "https://doccano.notaningress.com/v1/auth/login/")
        self.assertEqual(self.client.api_url, "https://doccano.notaningress.com/v1")

    @responses.activate
    def test_client_login(self):
        def request_callback(request):
            payload = json.loads(request.body)
            headers = {"request-id": "unique_id_a"}
            if payload["username"] != "good_username" or payload["password"] != "good_password":
                return (403, headers, json.dumps(payload))

            response_body = {"key": "valid_token"}
            return (200, headers, json.dumps(response_body))

        responses.add_callback(
            responses.POST,
            "https://doccano.notaningress.com/v1/auth/login/",
            callback=request_callback,
            content_type="application/json",
        )

        context = None
        with self.assertRaises(DoccanoAPIError) as context:
            self.client.login("some_user", "some_pass")

        self.assertEqual(context.exception.response.status_code, 403)

        self.client.login("good_username", "good_password")
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].response.status_code, 200)

    def test_client_projects(self):
        projects = self.client.projects

        self.assertIs(projects.client_session, self.client.client_session)
        # Disable protected-access check for test case
        self.assertEqual(projects._api_url, self.client.api_url)  # pylint: disable=protected-access

    @responses.activate
    def test_can_access_nested_project_elements(self):
        responses.add(mock_projects.projects_get_response)
        responses.add(mock_examples.example_create_response)
        create_example = Example(text="This is a test example")

        my_project_controller = next(
            proj_controller
            for proj_controller in self.client.projects.all()
            if proj_controller.project.name == "somethingsomething3"
        )
        created_example = my_project_controller.examples.create(create_example)

        self.assertEqual(created_example.id, 49)
