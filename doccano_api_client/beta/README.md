# Doccano API BETA Client

A beta version of a new design for the Doccano client, featuring more Pythonic interaction, as well as thorough testing and documentation.

Currently tested for compatibility against Doccano v1.5.0-1.5.5.

### Usage

The client can be instatiated with a base URL referring to the target Doccano instance. Once instantiated, you can login using your Doccano username and password.

```python
from doccano_api_client.beta import DoccanoClient, controllers

client = DoccanoClient("your_instance_url_here")
client.login("my_username", "my_password")
```

Once the client is instantiated and a session login to Doccano is established, you can access your projects with Python-ized navigation.

```python
project_controllers = client.projects.all()

my_project_name_controller = next(controller for controller in project_controllers if controller.project.name == "My Project Name")

my_example = models.Example(text="This is an example text")
my_project_name_controller.examples.create(my_example)

```

### Running local integration tests
Given that the Doccano project can get updated with API-breaking changes, we introduced the ability to run local integration tests against all the main endpoints.
This allows to make sure that our client is still operational with newer Doccano versions.

To run the integration tests:
- Spin up doccano locally. Clone the Doccano repo, and deploy or stand up your Doccano instance
- Then, within the root of this repo, run
```shell
pipenv run test --runintegrationtest
```

## Potential Additions

- Upgrade to 1.6.x compatibility
- Potentially adding Pydantic for tighter field validation
- Add missing functionality that the primary Doccano client offers
