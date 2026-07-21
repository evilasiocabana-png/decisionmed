"""Editorial workflow for scientific knowledge packages."""

from scientific_knowledge.models import KnowledgePackage, ReviewerRecord


class EditorialPipeline:
    """Advance package metadata through allowed editorial states."""

    stages: tuple[str, ...] = (
        "draft",
        "review",
        "scientific_review",
        "editorial_approval",
        "published",
        "deprecated",
    )

    def next_stage(self, current_stage: str) -> str:
        if current_stage not in self.stages:
            return "draft"
        index = self.stages.index(current_stage)
        if index >= len(self.stages) - 1:
            return current_stage
        return self.stages[index + 1]

    def can_publish(self, package: KnowledgePackage) -> bool:
        return package.publication_status == "editorial_approval"


class ScientificReviewerRegistry:
    """In-memory reviewer registry for future editorial review."""

    def __init__(self) -> None:
        self._reviewers: dict[str, ReviewerRecord] = {}

    def register(self, reviewer: ReviewerRecord) -> None:
        self._reviewers[reviewer.reviewer_id] = reviewer

    def list_reviewers(self) -> tuple[ReviewerRecord, ...]:
        return tuple(self._reviewers.values())

