import vcr

from doccano_client.client import DoccanoClient
from doccano_client.clients.task_status import TaskStatusClient
from tests.conftest import cassettes_path


class TestTaskStatusClient:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(cassettes_path / "task_status/login.yaml"), mode="once"):
            client = DoccanoClient("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = TaskStatusClient(client)

    def test_get(self):
        with vcr.use_cassette(str(cassettes_path / "task_status/list.yaml"), mode="once"):
            task_id = "2a49f2cf-5508-45d3-b75e-d1dd2489aaf8"
            self.client.get(task_id)
