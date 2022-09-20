from dataclasses import dataclass, fields
from typing import Iterable

from requests import Session

from ..models import Project, Relation
from ..utils.response import verbose_raise_for_status


@dataclass
class RelationController:
    """Wraps an Relation."""

    id: int
    relation: Relation
    relations_url: str
    client_session: Session
    project: Project


class RelationsController:
    """Controls the creation and retrieval of individual annotations for an example."""

    def __init__(self, example_id: int, project: Project, example_url: str, client_session: Session):
        """Initializes a RelationsController instance

        Args:
            example_id: int. The relevant example id to this annotations controller
            example_url: str. Url of the parent example
            project: Project. The project model of the annotations, which is needed to query
                for the type of annotation used by the project.
            client_session: requests.session. The current session passed from client to models
        """
        self.example_id = example_id
        self.project = project
        self._example_url = example_url
        self.client_session = client_session

    @property
    def relations_url(self) -> str:
        """Return an api url for annotations list of a example"""
        return f"{self._example_url}/relations"

    def all(self) -> Iterable[RelationController]:
        """Return a sequence of RelationControllers."""
        response = self.client_session.get(self.relations_url)

        verbose_raise_for_status(response)
        relation_dicts = response.json()
        relation_obj_fields = set(relation_field.name for relation_field in fields(Relation))

        for relation_dict in relation_dicts:
            # Sanitize span_dict before converting to Example
            sanitized_relation_dict = {
                relation_Key: relation_dict[relation_Key] for relation_Key in relation_obj_fields
            }

            yield RelationController(
                relation=Relation(**sanitized_relation_dict),
                project=self.project,
                id=relation_dict["id"],
                relations_url=self.relations_url,
                client_session=self.client_session,
            )
