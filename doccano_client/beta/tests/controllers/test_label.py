from unittest import TestCase

import responses
from requests import Session

from ...controllers import LabelController, LabelsController
from ...controllers.label import LabelGenerator
from ...models import LABEL_COLOR_CYCLE, Label
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import labels as mocks


class LabelGeneratorTest(TestCase):
    def setUp(self):
        self.label_generator = LabelGenerator()

    def test_next_label_color(self):
        # Test color cycle once through
        for color in LABEL_COLOR_CYCLE:
            next_color = self.label_generator.next_label_color()
            self.assertEqual(next_color, color)

    def test_next_label_color_eventually_repeats_color(self):
        # Test color cycle once through
        for _ in LABEL_COLOR_CYCLE:
            self.label_generator.next_label_color()

        # Test that it starts back at the beginning after looping
        self.assertEqual(self.label_generator.next_label_color(), LABEL_COLOR_CYCLE[0])

    def test_next_label_shortcut_on_empty(self):
        with self.assertRaises(AssertionError):
            self.label_generator.next_label_shortcut("")

    def test_next_label_shortcut(self):
        text = "my_text"
        expected_shortcut = text.lower()[0]

        # Test that the first new shortcut is the first letter of the word
        shortcut = self.label_generator.next_label_shortcut(text)
        self.assertEqual(shortcut.prefix_key, None)
        self.assertEqual(shortcut.suffix_key, expected_shortcut)

        text = "my_different_text_but_same_first_letter"

        # The next generated shortcut on the same letter in the cycle includes a shift key
        shortcut = self.label_generator.next_label_shortcut(text)
        self.assertEqual(shortcut.prefix_key, "shift")
        self.assertEqual(shortcut.suffix_key, expected_shortcut)

        # The next generated on the same letter cycle through the digits as shortcuts
        for next_number in range(0, 10):
            shortcut = self.label_generator.next_label_shortcut(text)
            self.assertEqual(shortcut.prefix_key, None)
            self.assertEqual(shortcut.suffix_key, str(next_number))

        # The next generated after the digits is the digits with a shift key
        for next_number in range(0, 10):
            shortcut = self.label_generator.next_label_shortcut(text)
            self.assertEqual(shortcut.prefix_key, "shift")
            self.assertEqual(shortcut.suffix_key, str(next_number))
        # Check to make sure that, on many repeats, it will still return None when available
        # shortcuts have run out
        for _ in range(0, 20):
            shortcut = self.label_generator.next_label_shortcut(text)
            self.assertEqual(shortcut.prefix_key, None)
            self.assertEqual(shortcut.suffix_key, None)

        # But another first letter is still available
        second_text = "different_text"
        expected_shortcut = second_text.lower()[0]
        shortcut = self.label_generator.next_label_shortcut(second_text)
        self.assertEqual(shortcut.prefix_key, None)
        self.assertEqual(shortcut.suffix_key, expected_shortcut)

    def test_next_label(self):
        stock_label = Label(text="my text")
        self.assertEqual(stock_label.suffix_key, None)
        self.assertEqual(stock_label.prefix_key, None)
        self.assertEqual(stock_label.background_color, LABEL_COLOR_CYCLE[0])

        updated_label_a = self.label_generator.next_label(stock_label)
        self.assertEqual(updated_label_a.text, stock_label.text)
        self.assertEqual(updated_label_a.prefix_key, None)
        self.assertEqual(updated_label_a.suffix_key, "m")
        self.assertEqual(updated_label_a.background_color, LABEL_COLOR_CYCLE[0])

        updated_label_b = self.label_generator.next_label(stock_label)
        self.assertEqual(updated_label_b.text, stock_label.text)
        self.assertEqual(updated_label_b.prefix_key, "shift")
        self.assertEqual(updated_label_b.suffix_key, "m")
        self.assertEqual(updated_label_b.background_color, LABEL_COLOR_CYCLE[1])

    def test_new_generator_refreshes_all(self):
        stock_label = Label(text="my text")
        self.assertEqual(stock_label.suffix_key, None)
        self.assertEqual(stock_label.prefix_key, None)
        self.assertEqual(stock_label.background_color, LABEL_COLOR_CYCLE[0])

        updated_label_a = self.label_generator.next_label(stock_label)
        self.assertEqual(updated_label_a.text, stock_label.text)
        self.assertEqual(updated_label_a.prefix_key, None)
        self.assertEqual(updated_label_a.suffix_key, "m")
        self.assertEqual(updated_label_a.background_color, LABEL_COLOR_CYCLE[0])

        self.label_generator = LabelGenerator()
        updated_label_c = self.label_generator.next_label(stock_label)
        self.assertEqual(updated_label_c, updated_label_a)


class LabelControllerTest(TestCase):
    def setUp(self):
        self.label_a = Label(text="my text")
        self.label_controller_a = LabelController(
            label=self.label_a, id=43, labels_url="http://my_labels_url", client_session=Session()
        )

    def test_urls(self):
        self.assertEqual(self.label_controller_a.label_url, "http://my_labels_url/43")


class LabelsControllerTest(TestCase):
    def setUp(self):
        self.label_a = Label(text="next_test_label")
        self.label_controller_a = LabelController(
            label=self.label_a,
            id=43,
            labels_url="http://my_labels_url/v1/projects/23",
            client_session=Session(),
        )
        self.labels_controller = LabelsController("http://my_labels_url/v1/projects/23", Session())

    def test_controller_urls(self):
        self.assertEqual(self.labels_controller.labels_url, "http://my_labels_url/v1/projects/23/labels")

    @responses.activate
    def test_all_with_no_labels(self):
        responses.add(mocks.labels_get_empty_response)
        label_controllers = self.labels_controller.all()
        self.assertEqual(len(list(label_controllers)), 0)

    @responses.activate
    def test_all(self):
        responses.add(mocks.labels_get_response)
        label_controllers = self.labels_controller.all()

        total_labels = 0
        expected_label_id_dict = {label_json["id"]: label_json for label_json in mocks.labels_get_json}
        for label_controller in label_controllers:
            self.assertIn(label_controller.id, expected_label_id_dict)
            self.assertEqual(label_controller.label.text, expected_label_id_dict[label_controller.id]["text"])
            self.assertEqual(
                label_controller.label.suffix_key,
                expected_label_id_dict[label_controller.id]["suffix_key"],
            )
            self.assertIs(label_controller.client_session, self.labels_controller.client_session)
            total_labels += 1

        self.assertEqual(total_labels, len(mocks.labels_get_json))

    @responses.activate
    def test_all_with_bad_response(self):
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.labels_controller.all())

    @responses.activate
    def test_create(self):
        responses.add(mocks.label_create_response)
        label_a_controller = self.labels_controller.create(self.label_a)

        self.assertEqual(label_a_controller.id, mocks.label_create_json["id"])
        self.assertEqual(label_a_controller.label.text, mocks.label_create_json["text"])

    @responses.activate
    def test_create_with_bad_response(self):
        responses.add(bad.bad_post_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.labels_controller.create(self.label_a))

    @responses.activate
    def test_all_regenerated_with_no_labels(self):
        responses.add(mocks.labels_get_empty_response)
        label_controllers = self.labels_controller.all_regenerated()
        self.assertEqual(len(list(label_controllers)), 0)

    @responses.activate
    def test_all_regenerated(self):
        responses.add(mocks.labels_get_response)
        label_controllers = self.labels_controller.all_regenerated()

        next_color_cyle_index = 0
        for label_controller in label_controllers:
            self.assertEqual(label_controller.label.suffix_key, label_controller.label.text.lower()[0])
            self.assertEqual(label_controller.label.background_color, LABEL_COLOR_CYCLE[next_color_cyle_index])

            next_color_cyle_index += 1

    @responses.activate
    def test_update(self):
        responses.add(mocks.labels_get_response)
        responses.add(mocks.label_update_response)
        label_controllers = self.labels_controller.all_regenerated()
        self.labels_controller.update(label_controllers)

    @responses.activate
    def test_update_with_bad_response(self):
        responses.add(bad.bad_put_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.labels_controller.update([self.label_controller_a]))
