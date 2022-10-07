from unittest.mock import MagicMock

import pytest

from doccano_client.models.project import Project
from doccano_client.usecase.project import ProjectUseCase


@pytest.fixture
def payload():
    return {
        "id": 1,
        "name": "Test Project",
        "description": "Test project",
        "project_type": "SequenceLabeling",
        "guideline": "",
    }


class TestProjectUseCase:
    @classmethod
    def setup_method(cls):
        cls.project_repository = MagicMock()
        cls.project_usecase = ProjectUseCase(cls.project_repository)

    def test_find_by_id(self):
        self.project_usecase.find_by_id(1)
        self.project_repository.find_by_id.assert_called_once_with(1)

    def test_list(self):
        list(self.project_usecase.list())
        self.project_repository.list.assert_called_once()

    def test_create(self, payload):
        payload.pop("id")
        self.project_usecase.create(**payload)
        self.project_repository.create.assert_called_once_with(Project.parse_obj(payload))

    def test_update(self, payload):
        project = Project.parse_obj(payload)
        self.project_repository.find_by_id.return_value = project
        self.project_usecase.update(project_id=1, name="New Name")
        project.name = "New Name"
        self.project_repository.find_by_id.assert_called_once_with(1)
        self.project_repository.update.assert_called_once_with(project)

    def test_delete(self):
        self.project_usecase.delete(1)
        self.project_repository.delete.assert_called_once_with(1)
