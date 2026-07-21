"""Editorial review engine."""

from __future__ import annotations

from scientific_validation.models import EditorialDecision


class EditorialReviewEngine:
    STATES = ("pending", "under review", "approved", "revision required", "rejected")

    def decide(self, reviewers: tuple[str, ...], rationale: str, approved: bool = False) -> EditorialDecision:
        return EditorialDecision(
            state="approved" if approved else "under review",
            reviewers=reviewers,
            rationale=rationale or "editorial_rationale_required",
        )

