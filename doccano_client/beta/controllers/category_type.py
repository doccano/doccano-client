from dataclasses import asdict, dataclass, fields
from typing import Iterable

from requests import Session

from ..models.category_type import LABEL_COLOR_CYCLE, CategoryType
from ..utils.response import verbose_raise_for_status

COLOR_CYCLE_RANGE = len(LABEL_COLOR_CYCLE)


@dataclass
class CategoryTypeController:
    """Wraps a CategoryType with fields used for interacting directly with Doccano client"""

    category_type: CategoryType
    id: int
    category_types_url: str
    client_session: Session

    @property
    def category_type_url(self) -> str:
        """Return an api url for this category_type"""
        return f"{self.category_types_url}/{self.id}"


class CategoryTypesController:
    """Controls the creation and retrieval of individual CategoryTypeControllers for an assigned project"""

    def __init__(self, project_url: str, client_session: Session) -> None:
        """Initializes a CategoryTypeController instance"""
        self._project_url = project_url
        self.client_session = client_session

    @property
    def category_types_url(self) -> str:
        """Return an api url for category_types list"""
        return f"{self._project_url}/category-types"

    def all(self) -> Iterable[CategoryTypeController]:
        """Return a sequence of all category-types for a given controller, which maps to a project

        Yields:
            CategoryTypeController: The next category type controller.
        """
        response = self.client_session.get(self.category_types_url)
        verbose_raise_for_status(response)
        category_type_dicts = response.json()
        category_type_object_fields = set(category_type_field.name for category_type_field in fields(CategoryType))

        for category_type_dict in category_type_dicts:
            # Sanitize category_type_dict before converting to CategoryType
            sanitized_category_type_dict = {
                category_type_key: category_type_dict[category_type_key]
                for category_type_key in category_type_object_fields
            }

            yield CategoryTypeController(
                category_type=CategoryType(**sanitized_category_type_dict),
                id=category_type_dict["id"],
                category_types_url=self.category_types_url,
                client_session=self.client_session,
            )

    def create(self, category_type: CategoryType) -> CategoryTypeController:
        """Create new category_type for Doccano project, assign session variables to category_type, return the id"""
        category_type_json = asdict(category_type)

        response = self.client_session.post(self.category_types_url, json=category_type_json)
        verbose_raise_for_status(response)
        response_id = response.json()["id"]

        return CategoryTypeController(
            category_type=category_type,
            id=response_id,
            category_types_url=self.category_types_url,
            client_session=self.client_session,
        )

    def update(self, category_type_controllers: Iterable[CategoryTypeController]) -> None:
        """Updates the given category_types in the remote project"""
        for category_type_controller in category_type_controllers:
            category_type_json = asdict(category_type_controller.category_type)
            category_type_json = {
                category_type_key: category_type_value
                for category_type_key, category_type_value in category_type_json.items()
                if category_type_value is not None
            }
            category_type_json["id"] = category_type_controller.id

            response = self.client_session.put(category_type_controller.category_type_url, json=category_type_json)
            verbose_raise_for_status(response)
