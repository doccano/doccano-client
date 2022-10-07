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
        """Return a sequence of all span-types for a given controller, which maps to a project

        Yields:
            SpanTypeController: The next span type controller.
        """
        response = self.client_session.get(self.span_types_url)
        verbose_raise_for_status(response)
        span_type_dicts = response.json()
        span_type_object_fields = set(span_type_field.name for span_type_field in fields(SpanType))

        for span_type_dict in span_type_dicts:
            # Sanitize span_type_dict before converting to SpanType
            sanitized_span_type_dict = {
                span_type_key: span_type_dict[span_type_key] for span_type_key in span_type_object_fields
            }

            yield SpanTypeController(
                span_type=SpanType(**sanitized_span_type_dict),
                id=span_type_dict["id"],
                span_types_url=self.span_types_url,
                client_session=self.client_session,
            )

    def create(self, span_type: SpanType) -> SpanTypeController:
        """Create new span_type for Doccano project, assign session variables to span_type, return the id"""
        span_type_json = asdict(span_type)

        response = self.client_session.post(self.span_types_url, json=span_type_json)
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
        for span_type_controller in span_type_controllers:
            span_type_json = asdict(span_type_controller.span_type)
            span_type_json = {
                span_type_key: span_type_value
                for span_type_key, span_type_value in span_type_json.items()
                if span_type_value is not None
            }
            span_type_json["id"] = span_type_controller.id

            response = self.client_session.put(span_type_controller.span_type_url, json=span_type_json)
            verbose_raise_for_status(response)
