from typing import Iterator, List, Literal, Optional

from doccano_client.models.project import Project
from doccano_client.repositories.project import ProjectRepository

ProjectType = Literal[
    "DocumentClassification",
    "SequenceLabeling",
    "Seq2seq",
    "Speech2text",
    "ImageClassification",
    "BoundingBox",
    "Segmentation",
    "ImageCaptioning",
    "IntentDetectionAndSlotFilling",
]


class ProjectUseCase:
    def __init__(self, repository: ProjectRepository):
        self._repository = repository

    def find_by_id(self, project_id: int) -> Project:
        """Find a project by id

        Args:
            project_id (int): The id of the project to find

        Returns:
            Project: The found project
        """
        return self._repository.find_by_id(project_id)

    def list(self) -> Iterator[Project]:
        """Return all projects in which you are a member

        Yields:
            Project: The next project.
        """
        yield from self._repository.list()

    def create(
        self,
        name: str,
        project_type: ProjectType,
        description: str = "",
        guideline: str = "",
        random_order: bool = False,
        collaborative_annotation: bool = False,
        single_class_classification: bool = False,
        allow_overlapping: bool = False,
        grapheme_mode: bool = False,
        use_relation: bool = False,
        tags: Optional[List[str]] = None,
    ) -> Project:
        """Create a new project

        Args:
            name (str): The name of the project
            project_type (ProjectType): The type of the project
            description (str): The description of the project. Defaults to "".
            guideline (str): The annotation guideline. Defaults to "".
            random_order (bool): Whether to shuffle the uploaded data. Defaults to False.
            collaborative_annotation (bool): If True, a data can be annotated by multiple users. Defaults to False.
            single_class_classification (bool): If True, only one label can apply a data. Defaults to False.
            allow_overlapping (bool): If True, span overlapping is allowed. Defaults to False.
            grapheme_mode (bool): If True, count multi-byte characters as one character. Defaults to False.
            use_relation (bool): If True, relation labeling is allowed. Defaults to False.
            tags (Optional[List[str]], optional): The tags of the project. Defaults to None.

        Returns:
            Project: The created project
        """
        project = Project(
            name=name,
            description=description,
            guideline=guideline,
            project_type=project_type,
            random_order=random_order,
            collaborative_annotation=collaborative_annotation,
            single_class_classification=single_class_classification,
            allow_overlapping=allow_overlapping,
            grapheme_mode=grapheme_mode,
            use_relation=use_relation,
            tags=tags or [],
        )
        return self._repository.create(project)

    def update(
        self,
        project_id: int,
        name: str,
        project_type: ProjectType,
        description: str = "",
        guideline: str = "",
        random_order: bool = False,
        collaborative_annotation: bool = False,
        single_class_classification: bool = False,
        allow_overlapping: bool = False,
        grapheme_mode: bool = False,
        use_relation: bool = False,
        tags: Optional[List[str]] = None,
    ) -> Project:
        """Update a project

        Args:
            name (str): The name of the project
            project_type (ProjectType): The type of the project
            description (str): The description of the project. Defaults to "".
            guideline (str): The annotation guideline. Defaults to "".
            random_order (bool): Whether to shuffle the uploaded data. Defaults to False.
            collaborative_annotation (bool): If True, a data can be annotated by multiple users. Defaults to False.
            single_class_classification (bool): If True, only one label can apply a data. Defaults to False.
            allow_overlapping (bool): If True, span overlapping is allowed. Defaults to False.
            grapheme_mode (bool): If True, count multi-byte characters as one character. Defaults to False.
            use_relation (bool): If True, relation labeling is allowed. Defaults to False.
            tags (Optional[List[str]], optional): The tags of the project. Defaults to None.

        Returns:
            Project: The updated project
        """
        project = Project(
            id=project_id,
            name=name,
            description=description,
            guideline=guideline,
            project_type=project_type,
            random_order=random_order,
            collaborative_annotation=collaborative_annotation,
            single_class_classification=single_class_classification,
            allow_overlapping=allow_overlapping,
            grapheme_mode=grapheme_mode,
            use_relation=use_relation,
            tags=tags or [],
        )
        return self._repository.update(project)

    def delete(self, project_id: int):
        """Delete a project.

        Args:
            project_id (int): The project id.
        """
        self._repository.delete(project_id)
