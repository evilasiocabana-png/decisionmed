from dataclasses import dataclass
from datetime import datetime
import unittest

from decisionmed.domain import (
    BaseEntity,
    DomainError,
    DomainEvent,
    DomainInvariantError,
    DomainResult,
    EntityId,
    Repository,
    ResultAccessError,
    ValueObject,
)


class ExampleEntity(BaseEntity[EntityId]):
    pass


class OtherEntity(BaseEntity[EntityId]):
    pass


@dataclass(frozen=True, eq=False)
class ExampleValue(ValueObject):
    text: str

    @property
    def components(self) -> tuple[object, ...]:
        return (self.text,)


class MemoryRepository:
    def __init__(self) -> None:
        self.items: dict[EntityId, ExampleEntity] = {}

    def get(self, entity_id: EntityId) -> ExampleEntity | None:
        return self.items.get(entity_id)

    def add(self, entity: ExampleEntity) -> None:
        self.items[entity.id] = entity


class DomainCoreTest(unittest.TestCase):
    def test_entity_identity_is_stable_and_type_sensitive(self) -> None:
        identity = EntityId("entity-1")

        self.assertEqual(ExampleEntity(identity), ExampleEntity(identity))
        self.assertNotEqual(ExampleEntity(identity), OtherEntity(identity))
        with self.assertRaises(AttributeError):
            ExampleEntity(identity).id = EntityId("entity-2")  # type: ignore[misc]

    def test_entity_id_rejects_empty_or_excessive_values(self) -> None:
        with self.assertRaises(DomainInvariantError):
            EntityId(" ")
        with self.assertRaises(DomainInvariantError):
            EntityId("x" * 201)

    def test_value_object_uses_components_and_concrete_type(self) -> None:
        self.assertEqual(ExampleValue("same"), ExampleValue("same"))
        self.assertNotEqual(ExampleValue("same"), ExampleValue("different"))
        self.assertEqual(hash(ExampleValue("same")), hash(ExampleValue("same")))

    def test_domain_event_is_immutable_traceable_and_timezone_aware(self) -> None:
        event = DomainEvent(
            "workflow.started", "session-1", (("specialty", "cardiology"),)
        )

        self.assertTrue(event.event_id)
        self.assertIsNotNone(event.occurred_at.utcoffset())
        with self.assertRaises(AttributeError):
            event.name = "changed"  # type: ignore[misc]

    def test_domain_event_rejects_invalid_metadata(self) -> None:
        with self.assertRaises(DomainInvariantError):
            DomainEvent("Invalid Name", "session-1")
        with self.assertRaises(DomainInvariantError):
            DomainEvent("workflow.started", "session-1", (("key", "1"), ("key", "2")))
        with self.assertRaises(DomainInvariantError):
            DomainEvent(
                "workflow.started",
                "session-1",
                occurred_at=datetime(2026, 1, 1),
            )

    def test_result_exposes_exactly_one_side(self) -> None:
        success = DomainResult.success(None)
        failure = DomainResult.failure(DomainError("sample.failure", "failed"))

        self.assertTrue(success.is_success)
        self.assertIsNone(success.value)
        self.assertTrue(failure.is_failure)
        self.assertEqual("sample.failure", failure.error.code)
        with self.assertRaises(ResultAccessError):
            _ = success.error
        with self.assertRaises(ResultAccessError):
            _ = failure.value

    def test_repository_contract_is_structural(self) -> None:
        repository = MemoryRepository()
        entity = ExampleEntity(EntityId("entity-1"))
        repository.add(entity)

        self.assertIsInstance(repository, Repository)
        self.assertIs(entity, repository.get(entity.id))


if __name__ == "__main__":
    unittest.main()
