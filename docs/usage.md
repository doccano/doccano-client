# Usage

## Login

```python
from doccano_client.beta import DoccanoClient

client = DoccanoClient("your_instance_url_here")
client.login(username="username", password="password")
```

## Project

### Get a project

```python
project_controller = client.projects.get(project_id=1)
print(project_controller.project)
```

### List projects

```python
projects_controller = client.projects.all()
for controller in projects_controller:
    print(controller.project.name)
```

### Create a project

```py
from doccano_client.beta.models import Project, ProjectTypes

project = Project(
    name="My Project",
    description="My Project Description",
    project_type=ProjectTypes.DOCUMENT_CLASSIFICATION,
    guideline="Please write annotation guideline.",
    random_order=False,
    collaborative_annotation=False,
    single_class_classification=False
)
client.projects.create(project)
```

| Argument  | Required | Description  |
|---|---|---|
| `name`  | Yes | The project name  |
| `description`  | Yes | The project description  |
| `project_type`  | Yes | The type of the project. Choices are `DOCUMENT_CLASSIFICATION`, `SEQUENCE_LABELING`, and `Seq2seq`  |
| `guideline`  | No | The annotation guideline  |
| `random_order`  | No | Whether to show data in random order |
| `collaborative_annotation`  | No  | Share annotation with the project members |
| `single_class_classification`  | No  | Only one label can apply. Valid for classification projects only. |
| `allow_overlapping`  | No | Whether to allow overlapping spans. Valid for `SEQUENCE_LABELING` project only. |
| `grapheme_mode`  | No  | Handle multi-byte character like emoji(🌷, 💩, 👍), CRLF(\r\n) as a character. Valid for `SEQUENCE_LABELING` project only. |
| `use_relation`  | No  | Whether to use relation labeling. Valid for `SEQUENCE_LABELING` project only. |
