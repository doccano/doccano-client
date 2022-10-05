from dataclasses import asdict, dataclass, fields
from typing import Iterable

from requests import Session

from ..models import Project, Text
from ..utils.response import verbose_raise_for_status


@dataclass
class TextController:
    """Wraps a Text."""

    id: int
    text: Text
    texts_url: str
    client_session: Session
    project: Project


class TextsController:
    """Controls the creation and retrieval of individual annotations for an example."""

    def __init__(self, example_id: int, project: Project, example_url: str, client_session: Session):
        """Initializes a TextsController instance

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
    def texts_url(self) -> str:
        """Return an api url for annotations list of a example"""
        return f"{self._example_url}/texts"

    def all(self) -> Iterable[TextController]:
        """Return a sequence of TextControllers.

        Yields:
            TextController: The next text controller.
        """
        response = self.client_session.get(self.texts_url)
        verbose_raise_for_status(response)
        text_dicts = response.json()
        text_obj_fields = set(text_field.name for text_field in fields(Text))

        for text_dict in text_dicts:
            # Sanitize text_dict before converting to Example
            sanitized_text_dict = {text_key: text_dict[text_key] for text_key in text_obj_fields}

            yield TextController(
                text=Text(**sanitized_text_dict),
                project=self.project,
                id=text_dict["id"],
                texts_url=self.texts_url,
                client_session=self.client_session,
            )

    def create(self, text: Text) -> TextController:
        """Create a new text, return the generated controller

        Args:
            text: Text. Automatically assigns session variables.

        Returns:
            TextController. The TextController now wrapping around the newly created text.
        """
        text_json = asdict(text)

        response = self.client_session.post(self.texts_url, json=text_json)
        verbose_raise_for_status(response)
        response_id = response.json()["id"]

        return TextController(
            text=text,
            project=self.project,
            id=response_id,
            texts_url=self.texts_url,
            client_session=self.client_session,
        )
