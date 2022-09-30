import vcr

from doccano_client.client import DoccanoClient
from doccano_client.clients.metrics import MetricsClient
from doccano_client.models.metrics import LabelDistribution, MemberProgress, Progress
from tests.conftest import cassettes_path


class TestMetricsClient:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(cassettes_path / "metrics/login.yaml"), mode="once"):
            client = DoccanoClient("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = MetricsClient(client)
        cls.project_id = 16

    def test_get_progress(self):
        with vcr.use_cassette(str(cassettes_path / "metrics/progress.yaml"), mode="once"):
            response = self.client.get_progress(self.project_id)
        assert isinstance(response, Progress)

    def test_get_member_progress(self):
        with vcr.use_cassette(str(cassettes_path / "metrics/member_progress.yaml"), mode="once"):
            response = self.client.get_members_progress(self.project_id)
        assert all(isinstance(progress, MemberProgress) for progress in response)

    def test_get_category_distribution(self):
        with vcr.use_cassette(str(cassettes_path / "metrics/category_distribution.yaml"), mode="once"):
            response = self.client.get_category_distribution(self.project_id)
        assert all(isinstance(distribution, LabelDistribution) for distribution in response)
