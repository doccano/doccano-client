import time
from dataclasses import asdict, dataclass, fields
from typing import Any, Iterable

from requests import Session

from ..models.projects import Project
from ..utils.response import verbose_raise_for_status
from .comment import CommentsController
from .example import DocumentsController, ExamplesController
from .label import LabelsController
from .relation_type import RelationTypesController
from .span_type import SpanTypesController


@dataclass
class ProjectController:
    project: Project
    id: int
    projects_url: str
    client_session: Session

    @property
    def project_url(self) -> str:
        """Return an api url for this project"""
        return f"{self.projects_url}/{self.id}"

    @property
    def labels(self) -> LabelsController:
        """Return a LabelsController mapped to this project"""
        return LabelsController(self.project_url, self.client_session)

    # TODO: Retained for backwards compatibility. Remove in v1.6.0
    @property
    def documents(self) -> DocumentsController:
        """Return a DocumentsController mapped to this project"""
        return DocumentsController(self.project, self.project_url, self.client_session)

    @property
    def examples(self) -> ExamplesController:
        """Return a ExamplesController mapped to this project"""
        return ExamplesController(self.project, self.project_url, self.client_session)

    @property
    def comments(self) -> CommentsController:
        """Return a CommentsController mapped to this project"""
        return CommentsController(self.project_url, self.client_session)

    @property
    def span_types(self) -> SpanTypesController:
        """Return a SpanTypesController mapped to this project"""
        return SpanTypesController(self.project_url, self.client_session)

    @property
    def relation_types(self) -> RelationTypesController:
        """Return a RelationTypesController mapped to this project"""
        return RelationTypesController(self.project_url, self.client_session)

    def download(self, api_url: str, only_approved: bool = True) -> Iterable[Any]:
        """Trigger a download of all approved and labelled texts in jsonl format. It's zipped"""

        download_json = {"exportApproved": only_approved, "format": "JSONL"}
        responseCreateExportTask = self.client_session.post(
            f"{self.projects_url}/{self.id}/download", json=download_json
        )
        id_task = responseCreateExportTask.json()["task_id"]
        print("created export task: " + str(id_task))

        export_file = ""
        waitLoop = 0
        while waitLoop <= 300:
            waitLoop += 1
            responseTaskStatus = self.client_session.get(f"{api_url}/tasks/status/{id_task}")
            statusResult = responseTaskStatus.json()
            if statusResult["ready"] is True:
                export_file = statusResult["result"]
                break
            else:
                print(f"wait for export file: {waitLoop}sec.")
                time.sleep(1)

        print("export file: " + export_file)
        with self.client_session.get(f"{self.projects_url}/{self.id}/download?taskId={id_task}", stream=True) as r:
            r.raise_for_status()
            yield from r.iter_content(chunk_size=65536)


class ProjectsController:
    """Controls the retrieval of individual ProjectControllers"""

    __slots__ = ["_api_url", "client_session"]

    def __init__(self, api_url: str, client_session: Session):
        """Initializes a ProjectController instance"""
        self._api_url = api_url
        self.client_session = client_session

    @property
    def projects_url(self) -> str:
        """Return an api url for projects list"""
        return f"{self._api_url}/projects"

    def get(self, project_id: int) -> ProjectController:
        """Return a ProjectController for a given project id."""
        response = self.client_session.get(f"{self.projects_url}/{project_id}")
        verbose_raise_for_status(response)
        project_dict = response.json()

        return ProjectController(
            project=Project.from_dict(project_dict),
            id=project_dict["id"],
            projects_url=self.projects_url,
            client_session=self.client_session,
        )

    def all(self) -> Iterable[ProjectController]:
        """Return a sequence of projects for a given controller, assigned to the user"""
        response = self.client_session.get(self.projects_url)

        while True:
            verbose_raise_for_status(response)
            project_dicts = response.json()
            project_obj_fields = set(  # Only use fields that are part of the init, skips resourcetype
                proj_field.name for proj_field in fields(Project) if proj_field.init
            )

            for project_dict in project_dicts["results"]:
                # Sanitize project_dict before converting to Project
                sanitized_project_dict = {proj_key: project_dict[proj_key] for proj_key in project_obj_fields}

                yield ProjectController(
                    project=Project(**sanitized_project_dict),
                    id=project_dict["id"],
                    projects_url=self.projects_url,
                    client_session=self.client_session,
                )

            if project_dicts["next"] is None:
                break
            else:
                response = self.client_session.get(project_dicts["next"])

    def create(self, project: Project) -> ProjectController:
        """Create a new Doccano project, assign session variables to ProjectController, return it"""
        project_json = asdict(project)

        response = self.client_session.post(self.projects_url, json=project_json)
        verbose_raise_for_status(response)
        response_id = response.json()["id"]

        return ProjectController(
            project=project,
            id=response_id,
            projects_url=self.projects_url,
            client_session=self.client_session,
        )
