"""Registry that resolves every specialty field to governed knowledge."""

from __future__ import annotations

from collections.abc import Iterable

from .models import KnowledgeError, KnowledgeStatus
from .registry import KnowledgeRegistry
from .schemas import SpecialtyFormSchema


class SpecialtyFormSchemaRegistry:
    def __init__(
        self,
        knowledge: KnowledgeRegistry,
        schemas: Iterable[SpecialtyFormSchema] = (),
    ) -> None:
        if not isinstance(knowledge, KnowledgeRegistry):
            raise TypeError("knowledge must be a KnowledgeRegistry")
        self._knowledge = knowledge
        self._schemas: dict[str, SpecialtyFormSchema] = {}
        for schema in schemas:
            self.register(schema)

    def register(self, schema: SpecialtyFormSchema) -> SpecialtyFormSchema:
        if not isinstance(schema, SpecialtyFormSchema):
            raise TypeError("schema must be a SpecialtyFormSchema")
        if schema.specialty_key in self._schemas:
            raise KnowledgeError(
                "specialty_form_schema_registry.duplicate_specialty",
                f"schema already registered for: {schema.specialty_key}",
            )

        objects = tuple(
            self._knowledge.require(field.knowledge_object_id)
            for field in schema.fields
        )
        if schema.status is KnowledgeStatus.VALIDATED and any(
            item.status is not KnowledgeStatus.VALIDATED for item in objects
        ):
            raise KnowledgeError(
                "specialty_form_schema_registry.unvalidated_knowledge",
                "validated schema requires validated knowledge objects",
            )

        self._schemas[schema.specialty_key] = schema
        return schema

    def get(self, specialty_key: str) -> SpecialtyFormSchema | None:
        return self._schemas.get(specialty_key)

    def require(self, specialty_key: str) -> SpecialtyFormSchema:
        schema = self.get(specialty_key)
        if schema is None:
            raise KnowledgeError(
                "specialty_form_schema_registry.unknown",
                f"form schema not registered: {specialty_key}",
            )
        return schema

    def all(self) -> tuple[SpecialtyFormSchema, ...]:
        return tuple(self._schemas[key] for key in sorted(self._schemas))
