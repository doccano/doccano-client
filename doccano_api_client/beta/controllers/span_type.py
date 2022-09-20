from dataclasses import asdict, dataclass, fields
from typing import Iterable

from requests import Session

from ..models.span_type import LABEL_COLOR_CYCLE, SpanType
from ..utils.response import verbose_raise_for_status

COLOR_CYCLE_RANGE = len(LABEL_COLOR_CYCLE)


@dataclass
class SpanTypeController:
    """Wraps a SpanType with fields used for interacting directly with Doccano client"""

    span_type: SpanType
    id: int
    span_types_url: str
    client_session: Session

    @property
    def span_type_url(self) -> str:
        """Return an api url for this span_type"""
        return f"{self.span_types_url}/{self.id}"


class SpanTypesController:
    """Controls the creation and retrieval of individual SpanTypeControllers for an assigned project"""

    def __init__(self, project_url: str, client_session: Session) -> None:
        """Initializes a SpanTypeController instance"""
        self._project_url = project_url
        self.client_session = client_session

    @property
    def span_types_url(self) -> str:
        """Return an api url for span_types list"""
        return f"{self._project_url}/span-types"

    def all(self) -> Iterable[SpanTypeController]:
        """Return a sequence of all span-types for a given controller, which maps to a project"""
        response = self.client_session.get(self.span_types_url)
        verbose_raise_for_status(response)
        label_dicts = response.json()
        label_object_fields = set(label_field.name for label_field in fields(SpanType))

        for label_dict in label_dicts:
            # Sanitize label_dict before converting to Label
            sanitized_label_dict = {label_key: label_dict[label_key] for label_key in label_object_fields}

            yield SpanTypeController(
                span_type=SpanType(**sanitized_label_dict),
                id=label_dict["id"],
                span_types_url=self.span_types_url,
                client_session=self.client_session,
            )

    def create(self, span_type: SpanType) -> SpanTypeController:
        """Create new label for Doccano project, assign session variables to label, return the id"""
        label_json = asdict(span_type)

        response = self.client_session.post(self.span_types_url, json=label_json)
        verbose_raise_for_status(response)
        response_id = response.json()["id"]

        return SpanTypeController(
            span_type=span_type,
            id=response_id,
            span_types_url=self.span_types_url,
            client_session=self.client_session,
        )

    def update(self, span_type_controllers: Iterable[SpanTypeController]) -> None:
        """Updates the given span_types in the remote project"""
        for label_controller in span_type_controllers:
            label_json = asdict(label_controller.label)
            label_json = {
                label_key: label_value for label_key, label_value in label_json.items() if label_value is not None
            }
            label_json["id"] = label_controller.id

            response = self.client_session.put(label_controller.span_type_url, json=label_json)
            verbose_raise_for_status(response)
