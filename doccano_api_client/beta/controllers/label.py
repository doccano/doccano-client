from dataclasses import asdict, dataclass, fields
from typing import Iterable, NamedTuple, Optional, Set

from requests import Session

from ..models.labels import LABEL_COLOR_CYCLE, Label
from ..utils.response import verbose_raise_for_status

COLOR_CYCLE_RANGE = len(LABEL_COLOR_CYCLE)


class Shortcut(NamedTuple):
    """Represents a keyboard shortcut"""

    prefix_key: Optional[str] = None
    suffix_key: Optional[str] = None


class LabelGenerator:
    """Returns new generated label fields based on memory of previously picked fields

    In Doccano, if you create labels on a project manually, it can be difficult to intuitively
    color coordinate them and set shortcuts. The GUI for this is quite manual. This class
    is intended to provide methods for regenerating a full set of labels from a given project with
    color coordination and intuitively set labels based on the contents of a given label and
    previously generated values.
    """

    def __init__(self) -> None:
        """Initializes the LabelFieldPicker"""
        self.color_cycle_index: int = 0
        self.picked_letters: Set[str] = set()
        self.picked_shift_letters: Set[str] = set()
        self.next_number_picker: int = 0

    def next_label_color(self) -> str:
        """Returns the next color in a cycle of label highlights, bumps the index for next call"""
        next_color = LABEL_COLOR_CYCLE[self.color_cycle_index % COLOR_CYCLE_RANGE]
        self.color_cycle_index += 1
        return next_color

    def next_label_shortcut(self, label_text: str) -> Shortcut:
        """Returns the next label keyboard shortcut, logs newly set shortcut to avoid overlap

        If all available shortcuts are taken, return None

        Args:
            label_text: str. The text of the label, used for picking preferred shortcuts (first
                letter of the text)

        Returns:
            A Shortcut named tuple containing the calculated prefix and suffix key

        Raises:
            AssertionError: If the label_text is empty
        """
        if len(label_text) == 0:
            raise AssertionError("label_text is empty, must be non-empty")

        first_char = label_text[0].lower()

        # Check if the character shortcut alone is available
        if first_char not in self.picked_letters:
            self.picked_letters.add(first_char)
            return Shortcut(prefix_key=None, suffix_key=first_char)
        # Check if shift+character shortcut is available
        elif first_char not in self.picked_shift_letters:
            self.picked_shift_letters.add(first_char)
            return Shortcut(prefix_key="shift", suffix_key=first_char)
        # Check if the digits have not been cycled through once yet
        elif self.next_number_picker < 10:
            next_number = str(self.next_number_picker % 10)
            self.next_number_picker += 1
            return Shortcut(prefix_key=None, suffix_key=next_number)
        # Check if the digits have been cycled through only once
        elif self.next_number_picker < 20:
            next_number = str(self.next_number_picker % 10)
            self.next_number_picker += 1
            return Shortcut(prefix_key="shift", suffix_key=next_number)

        return Shortcut(prefix_key=None, suffix_key=None)

    def next_label(self, label: Label) -> Label:
        """Returns an updated Label with fields newly generated"""
        shortcut = self.next_label_shortcut(label.text)
        background_color = self.next_label_color()

        return Label(
            text=label.text,
            prefix_key=shortcut.prefix_key,
            suffix_key=shortcut.suffix_key,
            background_color=background_color,
        )


@dataclass
class LabelController:
    """Wraps a Label with fields used for interacting directly with Doccano client"""

    label: Label
    id: int
    labels_url: str
    client_session: Session

    @property
    def label_url(self) -> str:
        """Return an api url for this label"""
        return f"{self.labels_url}/{self.id}"


class LabelsController:
    """Controls the creation and retrieval of individual LabelControllers for an assigned project"""

    def __init__(self, project_url: str, client_session: Session) -> None:
        """Initializes a LabelController instance"""
        self._project_url = project_url
        self.client_session = client_session

    @property
    def labels_url(self) -> str:
        """Return an api url for labels list"""
        return f"{self._project_url}/labels"

    def all(self) -> Iterable[LabelController]:
        """Return a sequence of all labels for a given controller, which maps to a project"""
        response = self.client_session.get(self.labels_url)
        verbose_raise_for_status(response)
        label_dicts = response.json()
        label_object_fields = set(label_field.name for label_field in fields(Label))

        for label_dict in label_dicts:
            # Sanitize label_dict before converting to Label
            sanitized_label_dict = {label_key: label_dict[label_key] for label_key in label_object_fields}

            yield LabelController(
                label=Label(**sanitized_label_dict),
                id=label_dict["id"],
                labels_url=self.labels_url,
                client_session=self.client_session,
            )

    def create(self, label: Label) -> LabelController:
        """Create new label for Doccano project, assign session variables to label, return the id"""
        label_json = asdict(label)

        response = self.client_session.post(self.labels_url, json=label_json)
        verbose_raise_for_status(response)
        response_id = response.json()["id"]

        return LabelController(
            label=label,
            id=response_id,
            labels_url=self.labels_url,
            client_session=self.client_session,
        )

    def all_regenerated(self) -> Iterable[LabelController]:
        """Regenerates fields for all labels for a given controller, returns the full new set

        Retrieves list of current labels for a given project and uses existing keyboard
        shortcuts and colors in the picking process. This can be useful if you just created a
        group of labels in the Doccano GUI, and don't want to manually go through and hand-assign
        each label a color and a shortcut.

        Yields:
            Iterable[LabelController]: the sereis of newly regenerated labels
        """
        label_generator = LabelGenerator()
        for label_controller in self.all():
            yield LabelController(
                label=label_generator.next_label(label_controller.label),
                id=label_controller.id,
                labels_url=label_controller.labels_url,
                client_session=label_controller.client_session,
            )

    def update(self, label_controllers: Iterable[LabelController]) -> None:
        """Updates the given labels in the remote project"""
        for label_controller in label_controllers:
            label_json = asdict(label_controller.label)
            label_json = {
                label_key: label_value for label_key, label_value in label_json.items() if label_value is not None
            }
            label_json["id"] = label_controller.id

            response = self.client_session.put(label_controller.label_url, json=label_json)
            verbose_raise_for_status(response)
