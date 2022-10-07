import vcr

from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.member import MemberRepository
from doccano_client.repositories.project import ProjectRepository
from doccano_client.repositories.role import RoleRepository
from doccano_client.repositories.user import UserRepository
from doccano_client.usecase.member import MemberUseCase
from doccano_client.usecase.project import ProjectUseCase
from tests.conftest import usecase_fixtures


class TestMemberUseCase:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(usecase_fixtures / "login.yaml"), mode="once"):
            base = BaseRepository("http://localhost:8000")
            base.login(username="admin", password="password")
            cls.project = ProjectUseCase(ProjectRepository(base))
            cls.member = MemberUseCase(MemberRepository(base), UserRepository(base), RoleRepository(base))

    def list_members(self):
        with vcr.use_cassette(str(usecase_fixtures / "member/list.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            members = self.member.list(project.id)
            assert len(members) == 1

    def test_add_member(self):
        with vcr.use_cassette(str(usecase_fixtures / "member/add.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            self.member.add(project.id, "hironsan", "annotator")
            members = self.member.list(project.id)
            assert len(members) == 2

    def test_delete_member(self):
        with vcr.use_cassette(str(usecase_fixtures / "member/delete.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            member = self.member.add(project.id, "hironsan", "annotator")
            members = self.member.list(project.id)
            assert len(members) == 2
            self.member.delete(project.id, member.id)
            members = self.member.list(project.id)
            assert len(members) == 1

    def test_update_member(self):
        with vcr.use_cassette(str(usecase_fixtures / "member/update.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            member = self.member.add(project.id, "hironsan", "annotator")
            members = self.member.list(project.id)
            assert len(members) == 2
            self.member.update(project.id, member.id, "project_admin")
            members = self.member.list(project.id)
            assert len(members) == 2
            assert members[1].rolename == "project_admin"
