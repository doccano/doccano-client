from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, Iterable

from requests import Session

from ..models.examples import Example
from ..models.projects import Project
from ..utils.response import verbose_raise_for_status
from .comment import CommentsController
from .relation import RelationsController
from .span import SpansController

EXAMPLES_PER_PAGE_LIMIT = 10


@dataclass
class ExampleController:
    """Wraps a Example with fields used for interacting directly with Doccano client"""

    example: Example
    id: int
    examples_url: str
    client_session: Session
    project: Project

    @property
    def example_url(self) -> str:
        """Return an api url for this example"""
        return f"{self.examples_url}/{self.id}"

    @property
    def comments(self) -> CommentsController:
        """Return a CommentsController mapped to this example"""
        return CommentsController(self.example_url, self.client_session)

    @property
    def spans(self) -> SpansController:
        """Return an SpanController mapped to this example"""
        return SpansController(self.id, self.project, self.example_url, self.client_session)

    @property
    def relations(self) -> RelationsController:
        """Return an RelationController mapped to this example"""
        return RelationsController(self.id, self.project, self.example_url, self.client_session)


class ExamplesController:
    """Controls the creation and retrieval of individual ExampleControllers for a project"""

    def __init__(self, project: Project, project_url: str, client_session: Session) -> None:
        """Initializes a ExampleController instance"""
        self.project = project
        self._project_url = project_url
        self.client_session = client_session

    @property
    def examples_url(self) -> str:
        """Return an api url for examples list"""
        return f"{self._project_url}/examples"

    def _get_examples_response_from_api(
        self, page_index: int = 0, limit: int = EXAMPLES_PER_PAGE_LIMIT
    ) -> Dict[str, Any]:
        """Return the json response from an API call to get examples, handling pagination as well

        Args:
            page_index: int. Page number, starting at 0, for examples list to retrieve
            limit: int. examples-per-page limit set as an api query parameter

        Returns:
            json response from API call to Doccano instance
        """
        response = self.client_session.get(self.examples_url, params={"limit": limit, "offset": page_index * limit})
        verbose_raise_for_status(response)
        return response.json()

    def count(self) -> int:
        """Return the total number of examples for a project"""
        return self._get_examples_response_from_api(page_index=0, limit=1)["count"]

    def get(self, example_id: int) -> ExampleController:
        """Return a ExampleController given an id."""
        response = self.client_session.get(f"{self.examples_url}/{example_id}")
        verbose_raise_for_status(response)
        example_dict = response.json()

        return ExampleController(
            example=Example.from_dict(example_dict),
            project=self.project,
            id=example_dict["id"],
            examples_url=self.examples_url,
            client_session=self.client_session,
        )

    def all(self, confirmed=None) -> Iterable[ExampleController]:
        """Return a sequence of Examples for a given controller, which maps to a Project"""
        response = self.client_session.get(f"{self.examples_url}?confirmed={confirmed}")

        while True:
            verbose_raise_for_status(response)
            example_dicts = response.json()
            example_obj_fields = set(example_field.name for example_field in fields(Example))

            for example_dict in example_dicts["results"]:
                # Sanitize example_dict before converting to Example
                sanitized_example_dict = {example_key: example_dict[example_key] for example_key in example_obj_fields}

                yield ExampleController(
                    example=Example(**sanitized_example_dict),
                    project=self.project,
                    id=example_dict["id"],
                    examples_url=self.examples_url,
                    client_session=self.client_session,
                )

            if example_dicts["next"] is None:
                break
            else:
                response = self.client_session.get(example_dicts["next"])

    def create(self, example: Example) -> ExampleController:
        """Upload new example for Doccano project, return the generated controller

        Args:
            example: Example. The only fields that will be uploaded are text, annnotations,
                and meta.

        Returns:
            ExampleController. The ExampleController now wrapping around the newly created example
        """
        importable_keys = ["text", "meta"]
        example_as_dict = asdict(example)
        example_json = {importable_key: example_as_dict[importable_key] for importable_key in importable_keys}

        response = self.client_session.post(self.examples_url, json=example_json)
        verbose_raise_for_status(response)
        response_id = response.json()["id"]

        return ExampleController(
            example=example,
            project=self.project,
            id=response_id,
            examples_url=self.examples_url,
            client_session=self.client_session,
        )


# TODO: Retained for backwards compatibility. Remove in v1.6.0
DocumentController = ExampleController
DocumentsController = ExamplesController
