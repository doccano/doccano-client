from typing import Iterator, List

from doccano_client.models.comment import Comment
from doccano_client.repositories.comment import CommentRepository


class CommentUseCase:
    def __init__(self, repository: CommentRepository):
        self._repository = repository

    def find_by_id(self, project_id: int, comment_id: int) -> Comment:
        """Find a comment by id

        Args:
            project_id (int): The id of the project to find
            comment_id (int): The id of the comment to find

        Returns:
            Comment: The found comment
        """
        return self._repository.find_by_id(project_id, comment_id)

    def list(self, project_id: int, example_id: int, query: str = "") -> Iterator[Comment]:
        """Return all comments

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            query (str): The query string to filter comments

        Yields:
            Comment: The comments in the project.
        """
        yield from self._repository.list(project_id, example_id, query)

    def create(
        self,
        project_id: int,
        example_id: int,
        text: str,
    ) -> Comment:
        """Create a new comment

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            text (str): The text of the comment

        Returns:
            Comment: The created comment
        """
        comment = Comment(text=text, example=example_id)
        return self._repository.create(project_id, comment)

    def update(
        self,
        project_id: int,
        comment_id: int,
        text: str,
    ) -> Comment:
        """Update a comment

        Args:
            project_id (int): The id of the project
            comment_id (int): The id of the comment
            text (str): The text of the comment

        Returns:
            Comment: The updated comment
        """
        comment = self.find_by_id(project_id, comment_id)
        comment = Comment(id=comment.id, text=text, example=comment.example)
        return self._repository.update(project_id, comment)

    def delete(self, project_id: int, comment_id: int):
        """Delete a comment.

        Args:
            project_id (int): The project id.
            comment_id (int): The comment id.
        """
        self._repository.delete(project_id, comment_id)

    def bulk_delete(self, project_id: int, comment_ids: List[int]):
        """Bulk delete comments

        Args:
            project_id (int): The id of the project
            comment_ids (List[int]): The list of comment ids to delete
        """
        self._repository.bulk_delete(project_id, comment_ids)
