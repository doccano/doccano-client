from dataclasses import dataclass
from typing import Iterable

from requests import Session

from ..models import Annotation, Project
from ..utils.response import verbose_raise_for_status


@dataclass
class AnnotationController:
    """Wraps an Annotation."""

    id: int
    annotation: Annotation
    user: int
    created_at: str
    updated_at: str
    example: int


class AnnotationsController:
    """Controls the creation and retrieval of individual annotations for an example."""

    def __init__(self, example_id: int, project: Project, example_url: str, client_session: Session):
        """Initializes a AnnotationsController instance

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
    def annotations_url(self) -> str:
        """Return an api url for annotations list of a example"""
        return f"{self._example_url}"

    def all(self) -> Iterable[AnnotationController]:
        """Return a sequence of AnnotationControllers."""
        response = self.client_session.get(self.annotations_url)
        verbose_raise_for_status(response)
        annotation_dicts = response.json()["annotations"]

        for annotation_dict in annotation_dicts:
            yield AnnotationController(
                id=annotation_dict["id"],
                annotation=self.project.get_annotation_model().from_dict(annotation_dict),
                user=annotation_dict["user"],
                created_at=annotation_dict["created_at"],
                updated_at=annotation_dict["updated_at"],
                example=annotation_dict["example"],
            )
