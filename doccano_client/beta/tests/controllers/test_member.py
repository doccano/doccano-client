from unittest import TestCase

import responses
from requests import Session

from ...controllers import MemberController, MembersController
from ...models import Member
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import members as mocks


class MemberControllerTest(TestCase):
    def setUp(self):
        self.member = Member(user=1, role=1)
        self.member_controller = MemberController(
            id=43,
            member=self.member,
            members_url="http://my_members_url",
            client_session=Session(),
        )

    def test_urls(self):
        self.assertEqual(self.member_controller.member_url, "http://my_members_url/43")


class MembersControllerTest(TestCase):
    def setUp(self) -> None:
        self.member_a = Member(user=3, role=3)
        self.member_controller_a = MemberController(
            id=43,
            member=self.member_a,
            members_url="http://my_members_url",
            client_session=Session(),
        )
        self.members_controller = MembersController(
            project_url="http://my_members_url/v1/projects/23",
            client_session=Session(),
        )

    def test_controller_urls(self):
        self.assertEqual(self.members_controller.members_url, "http://my_members_url/v1/projects/23/members")

    @responses.activate
    def test_all_with_no_members(self):
        responses.add(mocks.members_get_empty_response)
        member_controllers = self.members_controller.all()
        self.assertEqual(len(list(member_controllers)), 0)

    @responses.activate
    def test_all(self):
        responses.add(mocks.members_get_response)
        member_controllers = self.members_controller.all()

        total_members = 0
        expected_member_id_dict = {member_json["id"]: member_json for member_json in mocks.members_get_json}
        for member_controller in member_controllers:
            self.assertIn(member_controller.id, expected_member_id_dict)
            self.assertEqual(member_controller.member.user, expected_member_id_dict[member_controller.id]["user"])
            self.assertEqual(member_controller.member.role, expected_member_id_dict[member_controller.id]["role"])
            self.assertIs(member_controller.client_session, self.members_controller.client_session)
            total_members += 1

        self.assertEqual(total_members, len(mocks.members_get_json))

    @responses.activate
    def test_all_with_bad_response(self):
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.members_controller.all())

    @responses.activate
    def test_create(self):
        responses.add(mocks.member_create_response)
        member_a_controller = self.members_controller.create(self.member_a)

        self.assertEqual(member_a_controller.id, mocks.member_create_json["id"])
        self.assertEqual(member_a_controller.member.user, mocks.member_create_json["user"])

    @responses.activate
    def test_create_with_bad_response(self):
        responses.add(bad.bad_post_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.members_controller.create(self.member_a))

    @responses.activate
    def test_update(self):
        responses.add(mocks.members_get_response)
        responses.add(mocks.member_update_response)
        member_controllers = self.members_controller.all()
        self.members_controller.update(member_controllers)

    @responses.activate
    def test_update_with_bad_response(self):
        responses.add(bad.bad_put_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.members_controller.update([self.member_controller_a]))
