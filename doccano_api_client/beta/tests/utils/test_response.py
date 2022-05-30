import re
from unittest import TestCase

import requests
import responses

from ...utils.response import DoccanoAPIError, verbose_raise_for_status


class ResponseTest(TestCase):
    @responses.activate
    def test_verbose_raise_for_status_does_nothing_for_good_status(self):
        responses.add("GET", url=re.compile(".*"), json={"detail": "something"}, status=200)
        resp = requests.get("http://mockurlplace.com")
        self.assertEqual(verbose_raise_for_status(resp), resp)

    @responses.activate
    def test_verbose_raise_for_status_adds_new_details(self):
        responses.add("GET", url=re.compile(".*"), json={"detail": "something bad"}, status=400)
        resp = requests.get("http://mockurlplace.com")

        context = None
        with self.assertRaises(DoccanoAPIError) as context:
            verbose_raise_for_status(resp)

        self.assertEqual(str(context.exception), "{'detail': 'something bad'}")
