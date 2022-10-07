from unittest.mock import MagicMock

import pytest

from doccano_client.models.project import Project
from doccano_client.repositories.project import ProjectRepository


@pytest.fixture
def response():
    return {
        "id": 1,
        "name": "Test Project",
        "description": "Test project",
        "project_type": "SequenceLabeling",
    }


class TestProjectRepository:
    def test_find_by_id(self, response):
        client = MagicMock()
        client.get.return_value.json.return_value = response
        project_client = ProjectRepository(client)
        project = project_client.find_by_id(1)
        assert project.id == 1

    def test_create(self, response):
        client = MagicMock()
        client.post.return_value.json.return_value = response
        project_client = ProjectRepository(client)
        project = project_client.create(Project.parse_obj(response))
        assert project.id == 1

    def test_update(self, response):
        client = MagicMock()
        client.put.return_value.json.return_value = response.copy()
        project_client = ProjectRepository(client)
        response["name"] = "Updated Project"
        project = Project.parse_obj(response)
        project = project_client.update(project)
        assert project.id == 1
        assert project.name == "Test Project"

    def test_delete(self):
        client = MagicMock()
        project_client = ProjectRepository(client)
        project_client.delete(1)
        client.delete.assert_called_once_with("projects/1")
