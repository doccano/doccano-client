from __future__ import annotations

from typing import Iterator, List

from doccano_client.models.metrics import (
    LabelCount,
    LabelDistribution,
    MemberProgress,
    Progress,
)
from doccano_client.repositories.base import BaseRepository


class MetricsRepository:
    """Repository for interacting with the Doccano metrics API"""

    def __init__(self, client: BaseRepository):
        self._client = client

    def get_progress(self, project_id: int) -> Progress:
        """Get my progress

        Args:
            project_id (int): The id of the project

        Returns:
            Progress: Your progress
        """
        resource = f"projects/{project_id}/metrics/progress"
        response = self._client.get(resource).json()
        return Progress(total=response["total"], completed=response["complete"], remaining=response["remaining"])

    def get_members_progress(self, project_id: int) -> List[MemberProgress]:
        """Return all metricss in which you are a member

        Args:
            project_id (int): The id of the project

        Returns:
            List[MemberProgress]: The list of the member progress.
        """
        resource = f"projects/{project_id}/metrics/member-progress"
        response = self._client.get(resource).json()
        return [
            MemberProgress(
                username=progress["user"],
                progress=Progress(
                    total=response["total"], completed=progress["done"], remaining=response["total"] - progress["done"]
                ),
            )
            for progress in response["progress"]
        ]

    def _get_label_distribution(self, resource: str) -> Iterator[LabelDistribution]:
        """Yield label distribution

        Args:
            resource (str): The resource to get

        Yields:
            LabelDistribution: The category distribution.
        """
        response = self._client.get(resource).json()
        for username, counts in response.items():
            label_counts = [LabelCount(label=label, count=count) for label, count in counts.items()]
            yield LabelDistribution(username=username, counts=label_counts)

    def get_category_distribution(self, project_id: int) -> List[LabelDistribution]:
        """Return category distribution

        Args:
            project_id (int): The id of the project

        Returns:
            LabelDistribution: The category distribution.
        """
        resource = f"projects/{project_id}/metrics/category-distribution"
        return list(self._get_label_distribution(resource))

    def get_span_distribution(self, project_id: int) -> List[LabelDistribution]:
        """Return span distribution

        Args:
            project_id (int): The id of the project

        Returns:
            LabelDistribution: The span distribution.
        """
        resource = f"projects/{project_id}/metrics/span-distribution"
        return list(self._get_label_distribution(resource))

    def get_relation_distribution(self, project_id: int) -> List[LabelDistribution]:
        """Return relation distribution

        Args:
            project_id (int): The id of the project

        Returns:
            LabelDistribution: The relation distribution.
        """
        resource = f"projects/{project_id}/metrics/relation-distribution"
        return list(self._get_label_distribution(resource))
