from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, Iterable

from requests import Session

from ..models.examples import Example
from ..models.projects import Project
from ..utils.response import verbose_raise_for_status
from .annotation import AnnotationsController
from .comment import CommentsController

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
    def annotations(self) -> AnnotationsController:
        """Return an AnnotationsController mapped to this example"""
        return AnnotationsController(self.id, self.project, self.example_url, self.client_session)


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
        response = self.client_session.get(
            self.examples_url, params={"limit": limit, "offset": page_index * limit}
        )
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

    def all(self) -> Iterable[ExampleController]:
        """Return a sequence of Examples for a given controller, which maps to a Project"""
        example_obj_fields = set(example_field.name for example_field in fields(Example))
        # Examples are paginated in Doccano's API, so handle pagination with yields
        page_index = 0
        example_dicts = self._get_examples_response_from_api(page_index=page_index)["results"]

        # When there are no more examples to paginate through, "results" recieved will be empty
        # NOTE: The Doccano pagination API responses also have "next" field that can be used to
        #       query the next page url. The problem is, this is returning urls with "http"
        #       as the protocol even when the host is https, so we use this method for
        #       pagination instead
        #       This still works deterministically because on the API side, the example list
        #       view/api endpoint is explicitly ordered. For non-randomized example order, it's
        #       it's ordered by ID. For randomized order, it's ordered randomly but with a fixed
        #       seed (the requesting user's id).
        while len(example_dicts) != 0:
            # Given a single page, iterate through the dicts on that page
            for example_dict in example_dicts:
                # TODO (louis): make a Example.from_json() method to handle this. Also, do this
                #               for all other models
                # Sanitize example_dict before converting to Example
                sanitized_example_dict = {
                    example_key: example_dict[example_key] for example_key in example_obj_fields
                }

                yield ExampleController(
                    example=Example(**sanitized_example_dict),
                    project=self.project,
                    id=example_dict["id"],
                    examples_url=self.examples_url,
                    client_session=self.client_session,
                )

            page_index += 1
            example_dicts = self._get_examples_response_from_api(page_index=page_index)["results"]

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
        example_json = {
            importable_key: example_as_dict[importable_key] for importable_key in importable_keys
        }

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
