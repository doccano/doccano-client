import re

import responses

generic_bad_response = {"detail": "Mock 400 Response Hit"}

bad_get_response = responses.Response(method="GET", url=re.compile(".*"), json=generic_bad_response, status=400)
bad_post_response = responses.Response(method="POST", url=re.compile(".*"), json=generic_bad_response, status=400)
bad_put_response = responses.Response(method="PUT", url=re.compile(".*"), json=generic_bad_response, status=400)
