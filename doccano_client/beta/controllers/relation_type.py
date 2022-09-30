from dataclasses import asdict, dataclass, fields
from typing import Iterable

from requests import Session

from ..models.relation_type import LABEL_COLOR_CYCLE, RelationType
from ..utils.response import verbose_raise_for_status

COLOR_CYCLE_RANGE = len(LABEL_COLOR_CYCLE)


@dataclass
class RelationTypeController:
    """Wraps a RelationType with fields used for interacting directly with Doccano client"""

    relation_type: RelationType
    id: int
    relation_types_url: str
    client_session: Session

    @property
    def relation_type_url(self) -> str:
        """Return an api url for this relation_type"""
        return f"{self.relation_types_url}/{self.id}"


class RelationTypesController:
    """Controls the creation and retrieval of individual RelationTypeControllers for an assigned project"""

    def __init__(self, project_url: str, client_session: Session) -> None:
        """Initializes a RelationTypeController instance"""
        self._project_url = project_url
        self.client_session = client_session

    @property
    def relation_types_url(self) -> str:
        """Return an api url for relation_types list"""
        return f"{self._project_url}/relation-types"

    def all(self) -> Iterable[RelationTypeController]:
        """Return a sequence of all relation-types for a given controller, which maps to a project

        Yields:
            RelationTypeController: The next relation type controller.
        """
        response = self.client_session.get(self.relation_types_url)
        verbose_raise_for_status(response)
        relation_type_dicts = response.json()
        relation_type_object_fields = set(relation_type_field.name for relation_type_field in fields(RelationType))

        for relation_type_dict in relation_type_dicts:
            # Sanitize relation_type_dict before converting to RelationType
            sanitized_relation_type_dict = {
                relation_type_key: relation_type_dict[relation_type_key]
                for relation_type_key in relation_type_object_fields
            }

            yield RelationTypeController(
                relation_type=RelationType(**sanitized_relation_type_dict),
                id=relation_type_dict["id"],
                relation_types_url=self.relation_types_url,
                client_session=self.client_session,
            )

    def create(self, relation_type: RelationType) -> RelationTypeController:
        """Create new relation_type for Doccano project, assign session variables to relation_type, return the id"""
        relation_type_json = asdict(relation_type)

        response = self.client_session.post(self.relation_types_url, json=relation_type_json)
        verbose_raise_for_status(response)
        response_id = response.json()["id"]

        return RelationTypeController(
            relation_type=relation_type,
            id=response_id,
            relation_types_url=self.relation_types_url,
            client_session=self.client_session,
        )

    def update(self, relation_type_controllers: Iterable[RelationTypeController]) -> None:
        """Updates the given relation_types in the remote project"""
        for relation_type_controller in relation_type_controllers:
            relation_type_json = asdict(relation_type_controller.relation_type)
            relation_type_json = {
                relation_type_key: relation_type_value
                for relation_type_key, relation_type_value in relation_type_json.items()
                if relation_type_value is not None
            }
            relation_type_json["id"] = relation_type_controller.id

            response = self.client_session.put(relation_type_controller.relation_type_url, json=relation_type_json)
            verbose_raise_for_status(response)
