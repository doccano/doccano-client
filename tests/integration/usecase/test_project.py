import pytest
import vcr

from doccano_client.models.project import Project
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.project import ProjectRepository
from doccano_client.usecase.project import ProjectUseCase
from tests.conftest import usecase_fixtures


class TestProjectUseCase:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(usecase_fixtures / "login.yaml"), mode="once"):
            base = BaseRepository("http://localhost:8000")
            base.login(username="admin", password="password")
            cls.usecase = ProjectUseCase(ProjectRepository(base))

    def test_list_projects(self):
        with vcr.use_cassette(str(usecase_fixtures / "project/list.yaml"), mode="once"):
            projects = self.usecase.list()
            assert all(isinstance(project, Project) for project in projects)

    def test_find_project_by_id(self):
        with vcr.use_cassette(str(usecase_fixtures / "project/find_by_id.yaml"), mode="once"):
            project = self.usecase.create(name="test", project_type="DocumentClassification", description="test")
            found_project = self.usecase.find_by_id(project.id)
            assert project == found_project

    def test_update_project(self):
        with vcr.use_cassette(str(usecase_fixtures / "project/update.yaml"), mode="once"):
            project = self.usecase.create(name="test", project_type="DocumentClassification", description="test")
            project.name = "test2"
            updated_project = self.usecase.update(project.id, name="test2")
            assert project == updated_project

    def test_delete_project(self):
        with vcr.use_cassette(str(usecase_fixtures / "project/delete.yaml"), mode="once"):
            project = self.usecase.create(name="test", project_type="DocumentClassification", description="test")
            self.usecase.delete(project)
            with pytest.raises(Exception):
                self.usecase.find_by_id(project.id)
