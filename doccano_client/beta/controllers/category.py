from dataclasses import asdict, dataclass, fields
from typing import Iterable

from requests import Session

from ..models import Category, Project
from ..utils.response import verbose_raise_for_status


@dataclass
class CategoryController:
    """Wraps a Category."""

    id: int
    category: Category
    categories_url: str
    client_session: Session
    project: Project


class CategoriesController:
    """Controls the creation and retrieval of individual annotations for an example."""

    def __init__(self, example_id: int, project: Project, example_url: str, client_session: Session):
        """Initializes a CategoriesController instance

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
    def categories_url(self) -> str:
        """Return an api url for annotations list of a example"""
        return f"{self._example_url}/categories"

    def all(self) -> Iterable[CategoryController]:
        """Return a sequence of CategoryControllers.

        Yields:
            CategoryController: The next category controller.
        """
        response = self.client_session.get(self.categories_url)
        verbose_raise_for_status(response)
        category_dicts = response.json()
        category_obj_fields = set(category_field.name for category_field in fields(Category))

        for category_dict in category_dicts:
            # Sanitize category_dict before converting to Example
            sanitized_category_dict = {
                category_key: category_dict[category_key] for category_key in category_obj_fields
            }

            yield CategoryController(
                category=Category(**sanitized_category_dict),
                project=self.project,
                id=category_dict["id"],
                categories_url=self.categories_url,
                client_session=self.client_session,
            )

    def create(self, category: Category) -> CategoryController:
        """Create a new category, return the generated controller

        Args:
            category: Category. Automatically assigns session variables.

        Returns:
            CategoryController. The CategoryController now wrapping around the newly created category.
        """
        category_json = asdict(category)

        response = self.client_session.post(self.categories_url, json=category_json)
        verbose_raise_for_status(response)
        response_id = response.json()["id"]

        return CategoryController(
            category=category,
            project=self.project,
            id=response_id,
            categories_url=self.categories_url,
            client_session=self.client_session,
        )
