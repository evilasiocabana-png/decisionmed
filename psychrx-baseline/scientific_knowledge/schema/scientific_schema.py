"""Factory for the Official Scientific Knowledge schema."""

from scientific_knowledge.models import ScientificKnowledgeSchema


def create_official_schema() -> ScientificKnowledgeSchema:
    """Return the canonical schema without adding clinical content."""
    return ScientificKnowledgeSchema()

