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
        """Return a sequence of all span-types for a given controller, which maps to a project"""
        response = self.client_session.get(self.relation_types_url)
        verbose_raise_for_status(response)
        label_dicts = response.json()
        label_object_fields = set(label_field.name for label_field in fields(RelationType))

        for label_dict in label_dicts:
            # Sanitize label_dict before converting to Label
            sanitized_label_dict = {label_key: label_dict[label_key] for label_key in label_object_fields}

            yield RelationTypeController(
                relation_type=RelationType(**sanitized_label_dict),
                id=label_dict["id"],
                relation_types_url=self.relation_types_url,
                client_session=self.client_session,
            )

    def create(self, relation_type: RelationType) -> RelationTypeController:
        """Create new label for Doccano project, assign session variables to label, return the id"""
        label_json = asdict(relation_type)

        response = self.client_session.post(self.relation_types_url, json=label_json)
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
        for label_controller in relation_type_controllers:
            label_json = asdict(label_controller.label)
            label_json = {
                label_key: label_value for label_key, label_value in label_json.items() if label_value is not None
            }
            label_json["id"] = label_controller.id

            response = self.client_session.put(label_controller.relation_type_url, json=label_json)
            verbose_raise_for_status(response)
