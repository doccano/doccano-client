from __future__ import annotations

from typing import Iterator, List, Optional

from doccano_client.models.comment import Comment
from doccano_client.repositories.base import BaseRepository


class CommentRepository:
    """Repository for interacting with the Doccano comment API"""

    resource_type = "comments"

    def __init__(self, client: BaseRepository):
        self._client = client

    def find_by_id(self, project_id: int, comment_id: int) -> Comment:
        """Find a comment by id

        Args:
            project_id (int): The id of the project
            comment_id (int): The id of the comment to find

        Returns:
            Comment: The found comment
        """
        response = self._client.get(f"projects/{project_id}/{self.resource_type}/{comment_id}")
        return Comment.parse_obj(response.json())

    def list(self, project_id: int, example_id: Optional[int] = None, query: str = "") -> Iterator[Comment]:
        """Return all comments in which you are a member

        Args:
            project_id (int): The id of the project
            example_id (Optional[int], optional): The id of the example. Defaults to None.
            query (str): The query to search. Defaults to None.

        Yields:
            Comment: The list of the comments.
        """
        params = {"example": example_id, "q": query}
        if not example_id:
            params.pop("example")

        response = self._client.get(f"projects/{project_id}/{self.resource_type}", params=params)
        while True:
            comments = response.json()
            for comment in comments["results"]:
                yield Comment.parse_obj(comment)

            if comments["next"] is None:
                break
            else:
                response = self._client.get(comments["next"])

    def create(self, project_id: int, comment: Comment) -> Comment:
        """Create a new comment

        Args:
            project_id (int): The id of the project
            comment (Comment): The comment to create

        Returns:
            Comment: The created comment
        """
        resource = f"projects/{project_id}/{self.resource_type}?example={comment.example}"
        response = self._client.post(resource, json=comment.dict(exclude={"id", "example"}))
        return Comment.parse_obj(response.json())

    def update(self, project_id: int, comment: Comment) -> Comment:
        """Update a comment

        Args:
            project_id (int): The id of the project
            comment (Comment): The comment to update

        Returns:
            Comment: The updated comment
        """
        resource = f"projects/{project_id}/{self.resource_type}/{comment.id}"
        response = self._client.put(resource, json=comment.dict())
        return Comment.parse_obj(response.json())

    def delete(self, project_id: int, comment: Comment | int):
        """Delete a comment

        Args:
            project_id (int): The id of the project
            comment (Comment | int): The comment to delete
        """
        comment_id = comment if isinstance(comment, int) else comment.id
        resource = f"projects/{project_id}/{self.resource_type}/{comment_id}"
        self._client.delete(resource)

    def bulk_delete(self, project_id: int, comments: List[int] | List[Comment]):
        """Bulk delete comments

        Args:
            project_id (int): The id of the project
            comments (List[int] | List[Comment]): The list of comment ids to delete
        """
        ids = [comment if isinstance(comment, int) else comment.id for comment in comments]
        self._client.delete(f"projects/{project_id}/{self.resource_type}", json={"ids": ids})
