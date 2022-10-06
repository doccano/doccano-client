# doccano client

A simple client wrapper for the doccano API.

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
user = doccano_client.get_profile()

# list all projects
projects = doccano_client.list_projects()
```

## Doccano API BETA Client

We're introducing a newly revamped Doccano API Client that features more Pythonic interaction as well as more testing and documentation. It also adds more regulated compatibility with specific Doccano release versions.

You can find the documentation on usage of the beta client [here](doccano_client/beta/README.md).
