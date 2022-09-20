from dataclasses import dataclass, fields
from typing import Iterable

from requests import Session

from ..models.comments import Comment
from ..utils.response import verbose_raise_for_status


@dataclass
class CommentController:
    """Wraps a Comment with fields used for interacting directly with Doccano client"""

    comment: Comment
    username: str
    created_at: str
    example: int
    id: int
    comments_url: str
    client_session: Session

    @property
    def comment_url(self) -> str:
        """Return an api url for this comment"""
        return f"{self.comments_url}/{self.id}"


class CommentsController:
    """Controls the creation and retrieval of CommentControllers for an object

    A noticeable ommission compared to other API list controllers is a create() method.
    While we could use the API to create new comments on examples, there is little to no
    reason seen for not discouraging it compared to commenting directly in the GUI.
    """

    def __init__(self, parent_url: str, client_session: Session) -> None:
        """Initializes a CommentsController instance

        Args:
            parent_url: str. Url of the parent model. Either a project or example can have a
                comments property. For a example, it's all of the comments on that example. For a
                project, it is all comments on all examples for a project.
            client_session: requests.session. The current session passed from client to models
        """
        self._parent_url = parent_url
        self.client_session = client_session

    @property
    def comments_url(self) -> str:
        """Return an api url for comments list of an object"""
        return f"{self._parent_url}/comments"

    def all(self) -> Iterable[CommentController]:
        """Return a sequence of Comments for a given controller, which maps to an object"""
        response = self.client_session.get(self.comments_url)
        verbose_raise_for_status(response)
        comment_dicts = response.json()
        comment_obj_fields = set(comment_field.name for comment_field in fields(Comment))

        for comment_dict in comment_dicts:
            # Sanitize comment_dict before converting to Comment
            sanitized_comment_dict = {comment_key: comment_dict[comment_key] for comment_key in comment_obj_fields}

            yield CommentController(
                comment=Comment(**sanitized_comment_dict),
                username=comment_dict["username"],
                created_at=comment_dict["created_at"],
                example=comment_dict["example"],
                id=comment_dict["id"],
                comments_url=self.comments_url,
                client_session=self.client_session,
            )
