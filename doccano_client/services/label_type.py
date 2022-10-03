from doccano_client.models.label_type import LabelType
from doccano_client.repositories.label_type import LabelTypeRepository


class LabelTypeService:
    def __init__(self, repository: LabelTypeRepository):
        self._repository = repository

    def exists(self, project_id: int, label_type: LabelType) -> bool:
        """Check if the label type exists

        Args:
            project_id (int): The id of the project
            label_type (LabelType): The label type to check

        Returns:
            bool: True if the label type exists, False otherwise
        """
        label_types = self._repository.list(project_id)
        for label_type_ in label_types:
            if label_type_.text == label_type.text and label_type_.id != label_type.id:
                return True
            if label_type.prefix_key or label_type.suffix_key:
                if label_type_.id == label_type.id:
                    continue
                if label_type_.prefix_key == label_type.prefix_key and label_type_.suffix_key == label_type.suffix_key:
                    return True
        return False
