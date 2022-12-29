from dataclasses import asdict, dataclass, fields
from typing import Iterable

from requests import Session

from ..models.members import Member
from ..utils.response import verbose_raise_for_status


@dataclass
class MemberController:
    """Wraps a Member with fields used for interacting directly with Doccano client"""

    id: int
    member: Member
    members_url: str
    client_session: Session

    @property
    def member_url(self) -> str:
        """Return an api url for this member"""
        return f"{self.members_url}/{self.id}"


class MembersController:
    """Controls the assignment and retrieval of MemberControllers for a project"""

    def __init__(self, project_url: str, client_session: Session) -> None:
        """Initializes a MemberController instance"""
        self._project_url = project_url
        self.client_session = client_session

    @property
    def members_url(self) -> str:
        """Return an api url for members list"""
        return f"{self._project_url}/members"

    def all(self) -> Iterable[MemberController]:
        """Return a sequence of all members for a given controller, which maps to a project

        Yields:
            MemberController: The next member controller.
        """
        response = self.client_session.get(self.members_url)
        verbose_raise_for_status(response)
        member_dicts = response.json()
        member_object_fields = set(member_field.name for member_field in fields(Member))

        for member_dict in member_dicts:
            # Sanitize member_dict before converting to Member
            sanitized_member_dict = {member_key: member_dict[member_key] for member_key in member_object_fields}

            yield MemberController(
                member=Member(**sanitized_member_dict),
                id=member_dict["id"],
                members_url=self.members_url,
                client_session=self.client_session,
            )

    def create(self, member: Member) -> MemberController:
        """Create new member for Doccano project, assign session variables to member, return the id"""
        member_json = asdict(member)

        response = self.client_session.post(self.members_url, json=member_json)
        verbose_raise_for_status(response)
        response_id = response.json()["id"]

        return MemberController(
            member=member,
            id=response_id,
            members_url=self.members_url,
            client_session=self.client_session,
        )

    def update(self, member_controllers: Iterable[MemberController]) -> None:
        """Updates the given members in the remote project"""
        for member_controller in member_controllers:
            member_json = asdict(member_controller.member)
            member_json = {
                member_key: member_value for member_key, member_value in member_json.items() if member_value is not None
            }
            member_json["id"] = member_controller.id

            response = self.client_session.put(member_controller.member_url, json=member_json)
            verbose_raise_for_status(response)
