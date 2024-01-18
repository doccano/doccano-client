from __future__ import annotations

from typing import Any, Dict, Iterator

from doccano_client.models.project import Project
from doccano_client.repositories.base import BaseRepository, get_next_url


class ProjectRepository:
    """Repository for interacting with the Doccano project API"""

    def __init__(self, client: BaseRepository):
        self._client = client

    def _to_domain(self, response: Dict[str, Any]) -> Project:
        """Convert a response to a domain object

        Args:
            response (Dict[str, Any]): The response to convert

        Returns:
            Project: The converted project
        """
        response["tags"] = [tag["text"] for tag in response.get("tags", [])]
        return Project.parse_obj(response)

    def _to_persistent(self, project: Project) -> Dict[str, Any]:
        """Convert a domain object to a persistent object

        Args:
            project (Project): The project to convert

        Returns:
            Dict[str, Any]: The converted project
        """
        project_dict = project.dict()
        project_dict["tags"] = [{"text": tag} for tag in project_dict["tags"]]
        return project_dict

    def find_by_id(self, project_id: int) -> Project:
        """Find a project by id

        Args:
            project_id (int): The id of the project to find

        Returns:
            Project: The found project
        """
        response = self._client.get(f"projects/{project_id}")
        return self._to_domain(response.json())

    def list(self) -> Iterator[Project]:
        """Return all projects in which you are a member

        Yields:
            Project: The next project.
        """
        response = self._client.get("projects")
        initial_url = response.url

        while True:
            projects = response.json()
            for project in projects["results"]:
                yield self._to_domain(project)

            next_page = get_next_url(self._client.api_url, initial_url, projects)

            if next_page is None:
                break
            else:
                response = self._client.get(next_page)

    def create(self, project: Project) -> Project:
        """Create a new project

        Args:
            project (Project): The project to create

        Returns:
            Project: The created project
        """
        payload = self._to_persistent(project)
        payload.pop("id", None)
        response = self._client.post("projects", json=payload)
        return self._to_domain(response.json())

    def update(self, project: Project) -> Project:
        """Update a project

        Args:
            project (Project): The project to update

        Returns:
            Project: The updated project
        """
        resource = f"projects/{project.id}"
        payload = self._to_persistent(project)
        response = self._client.put(resource, json=payload)
        return self._to_domain(response.json())

    def delete(self, project: Project | int):
        """Delete a project

        Args:
            project (Project | int): The project to delete
        """
        resource = f"projects/{project if isinstance(project, int) else project.id}"
        self._client.delete(resource)
