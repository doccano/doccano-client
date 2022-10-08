# doccano client

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cf90190126b948e09362048b63600b06)](https://www.codacy.com/gh/doccano/doccano-client/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=doccano/doccano-client&amp;utm_campaign=Badge_Grade) [![Tests](https://github.com/doccano/doccano-client/actions/workflows/ci.yml/badge.svg)](https://github.com/doccano/doccano-client/actions/workflows/ci.yml)

A simple client for the doccano API.

## Installation

To install `doccano-client`, simply run:

```bash
pip install doccano-client
```

## Usage

```python
from doccano_client import DoccanoClient

# instantiate a client and log in to a Doccano instance
client = DoccanoClient('http://doccano.example.com')
client.login(username='username', password='password')

# get basic information about the authorized user
user = client.get_profile()

# list all projects
projects = client.list_projects()
```

Please see the [documentation](https://doccano.github.io/doccano-client/) for further details.

## Doccano API BETA Client

We're introducing a newly revamped Doccano API Client that features more Pythonic interaction as well as more testing and documentation. It also adds more regulated compatibility with specific Doccano release versions.

You can find the documentation on usage of the beta client [here](doccano_client/beta/README.md).
