from __future__ import annotations

from typing import Iterator

from doccano_client.models.project import Project
from doccano_client.repositories.base import BaseRepository


class ProjectRepository:
    """Repository for interacting with the Doccano project API"""

    def __init__(self, client: BaseRepository):
        self._client = client

    def find_by_id(self, project_id: int) -> Project:
        """Find a project by id

        Args:
            project_id (int): The id of the project to find

        Returns:
            Project: The found project
        """
        response = self._client.get(f"projects/{project_id}")
        return Project.parse_obj(response.json())

    def list(self) -> Iterator[Project]:
        """Return all projects in which you are a member

        Yields:
            Project: The next project.
        """
        response = self._client.get("projects")

        while True:
            projects = response.json()
            for project in projects["results"]:
                yield Project.parse_obj(project)

            if projects["next"] is None:
                break
            else:
                response = self._client.get(projects["next"])

    def create(self, project: Project) -> Project:
        """Create a new project

        Args:
            project (Project): The project to create

        Returns:
            Project: The created project
        """
        response = self._client.post("projects", json=project.dict(exclude={"id"}))
        return Project.parse_obj(response.json())

    def update(self, project: Project) -> Project:
        """Update a project

        Args:
            project (Project): The project to update

        Returns:
            Project: The updated project
        """
        resource = f"projects/{project.id}"
        response = self._client.put(resource, json=project.dict())
        return Project.parse_obj(response.json())

    def delete(self, project: Project | int):
        """Delete a project

        Args:
            project (Project | int): The project to delete
        """
        resource = f"projects/{project if isinstance(project, int) else project.id}"
        self._client.delete(resource)
