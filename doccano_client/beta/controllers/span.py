from dataclasses import asdict, dataclass, fields
from typing import Iterable

from requests import Session

from ..models import Project, Span
from ..utils.response import verbose_raise_for_status


@dataclass
class SpanController:
    """Wraps an Span."""

    id: int
    span: Span
    spans_url: str
    client_session: Session
    project: Project


class SpansController:
    """Controls the creation and retrieval of individual annotations for an example."""

    def __init__(self, example_id: int, project: Project, example_url: str, client_session: Session):
        """Initializes a SpansController instance

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
    def spans_url(self) -> str:
        """Return an api url for annotations list of a example"""
        return f"{self._example_url}/spans"

    def all(self) -> Iterable[SpanController]:
        """Return a sequence of SpanControllers."""
        response = self.client_session.get(self.spans_url)
        verbose_raise_for_status(response)
        span_dicts = response.json()
        span_obj_fields = set(span_field.name for span_field in fields(Span))

        for span_dict in span_dicts:
            # Sanitize span_dict before converting to Example
            sanitized_span_dict = {span_Key: span_dict[span_Key] for span_Key in span_obj_fields}

            yield SpanController(
                span=Span(**sanitized_span_dict),
                project=self.project,
                id=span_dict["id"],
                spans_url=self.spans_url,
                client_session=self.client_session,
            )

    def create(self, span: Span) -> SpanController:
        """Create a new span, return the generated controller

        Args:
            span: Span. The only fields that will be uploaded are text, annnotations, and meta.

        Returns:
            SpanController. The SpanController now wrapping around the newly created span.
        """
        span_json = asdict(span)

        response = self.client_session.post(self.spans_url, json=span_json)
        verbose_raise_for_status(response)
        response_id = response.json()["id"]

        return SpanController(
            span=span,
            project=self.project,
            id=response_id,
            spans_url=self.spans_url,
            client_session=self.client_session,
        )
