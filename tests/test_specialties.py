import unittest
from dataclasses import FrozenInstanceError, fields

from decisionmed.specialties import (
    PSYCHIATRY_PACK,
    DuplicateSpecialtyPackError,
    SpecialtyPack,
    SpecialtyPackRegistry,
    SpecialtyPackStatus,
    UnknownSpecialtyPackError,
    build_default_specialty_registry,
)


def make_pack(**overrides: object) -> SpecialtyPack:
    values: dict[str, object] = {
        "key": "test-specialty",
        "display_name": "Especialidade de teste",
        "version": "1.0.0",
        "workflow_contract": "test.workflow.v1",
        "safety_contract": "test.safety.v1",
        "evidence_policy": "test.evidence.v1",
        "knowledge_namespace": "test-knowledge",
        "audit_namespace": "test-audit",
        "required_capabilities": ("safety", "evidence", "audit"),
        "status": SpecialtyPackStatus.REFERENCE_ONLY,
    }
    values.update(overrides)
    return SpecialtyPack(**values)  # type: ignore[arg-type]


class SpecialtyPackContractTest(unittest.TestCase):
    def test_pack_schema_contains_only_composition_metadata(self) -> None:
        self.assertEqual(
            {
                "key",
                "display_name",
                "version",
                "workflow_contract",
                "safety_contract",
                "evidence_policy",
                "knowledge_namespace",
                "audit_namespace",
                "required_capabilities",
                "status",
            },
            {field.name for field in fields(SpecialtyPack)},
        )

    def test_pack_is_immutable_and_normalizes_capabilities(self) -> None:
        pack = make_pack(required_capabilities=["safety", "evidence"])

        self.assertEqual(("safety", "evidence"), pack.required_capabilities)
        with self.assertRaises(FrozenInstanceError):
            pack.display_name = "Outro nome"  # type: ignore[misc]

    def test_pack_rejects_invalid_identifiers_and_versions(self) -> None:
        with self.assertRaisesRegex(ValueError, "canonical lowercase identifier"):
            make_pack(key="Cardiology")
        with self.assertRaisesRegex(ValueError, "semantic versioning"):
            make_pack(version="v1")

    def test_pack_requires_unique_capabilities(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot contain duplicates"):
            make_pack(required_capabilities=("safety", "safety"))

    def test_pack_requires_explicit_lifecycle_status(self) -> None:
        with self.assertRaisesRegex(TypeError, "SpecialtyPackStatus"):
            make_pack(status="active")


class SpecialtyPackRegistryTest(unittest.TestCase):
    def test_default_registry_contains_reference_only_psychiatry(self) -> None:
        registry = build_default_specialty_registry()

        self.assertIs(PSYCHIATRY_PACK, registry.require("psychiatry"))
        self.assertEqual(6, len(registry.all()))
        self.assertEqual(SpecialtyPackStatus.REFERENCE_ONLY, PSYCHIATRY_PACK.status)
        self.assertFalse(PSYCHIATRY_PACK.is_clinically_active)
        self.assertIn("safety", PSYCHIATRY_PACK.required_capabilities)
        self.assertIn("evidence", PSYCHIATRY_PACK.required_capabilities)
        self.assertIn("audit", PSYCHIATRY_PACK.required_capabilities)

    def test_registry_rejects_duplicate_keys(self) -> None:
        pack = make_pack()
        registry = SpecialtyPackRegistry((pack,))

        with self.assertRaises(DuplicateSpecialtyPackError):
            registry.register(pack)

    def test_registry_reports_unknown_required_pack(self) -> None:
        with self.assertRaises(UnknownSpecialtyPackError):
            SpecialtyPackRegistry().require("unknown")

    def test_registry_returns_deterministic_order(self) -> None:
        registry = SpecialtyPackRegistry(
            (make_pack(key="zeta"), make_pack(key="alpha"))
        )

        self.assertEqual(["alpha", "zeta"], [pack.key for pack in registry.all()])


if __name__ == "__main__":
    unittest.main()
