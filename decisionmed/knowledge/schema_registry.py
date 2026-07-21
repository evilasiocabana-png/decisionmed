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
        self._by_id: dict[str, SpecialtyFormSchema] = {}
        self._by_binding: dict[tuple[str, str, str], SpecialtyFormSchema] = {}
        for schema in schemas:
            self.register(schema)

    def register(self, schema: SpecialtyFormSchema) -> SpecialtyFormSchema:
        if not isinstance(schema, SpecialtyFormSchema):
            raise TypeError("schema must be a SpecialtyFormSchema")
        if schema.schema_id in self._by_id:
            raise KnowledgeError(
                "specialty_form_schema_registry.duplicate_schema_id",
                f"schema id already registered: {schema.schema_id}",
            )
        binding = (schema.specialty_key, schema.workflow_id, schema.step_key)
        if binding in self._by_binding:
            raise KnowledgeError(
                "specialty_form_schema_registry.duplicate_binding",
                "workflow step already has a form schema",
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

        self._by_id[schema.schema_id] = schema
        self._by_binding[binding] = schema
        return schema

    def get(
        self, specialty_key: str, workflow_id: str, step_key: str
    ) -> SpecialtyFormSchema | None:
        return self._by_binding.get((specialty_key, workflow_id, step_key))

    def require(
        self, specialty_key: str, workflow_id: str, step_key: str
    ) -> SpecialtyFormSchema:
        schema = self.get(specialty_key, workflow_id, step_key)
        if schema is None:
            raise KnowledgeError(
                "specialty_form_schema_registry.unknown",
                "form schema not registered for workflow step",
            )
        return schema

    def for_workflow(
        self, specialty_key: str, workflow_id: str
    ) -> tuple[SpecialtyFormSchema, ...]:
        return tuple(
            sorted(
                (
                    schema
                    for (specialty, workflow, _), schema in self._by_binding.items()
                    if specialty == specialty_key and workflow == workflow_id
                ),
                key=lambda schema: (schema.step_key, schema.schema_id),
            )
        )

    def all(self) -> tuple[SpecialtyFormSchema, ...]:
        return tuple(self._by_id[key] for key in sorted(self._by_id))
