import unittest
from dataclasses import FrozenInstanceError, fields, replace

from decisionmed.composition import (
    CapabilityBinding,
    DuplicateCapabilityBindingError,
    SpecialtyLoadResult,
    SpecialtyLoadStatus,
    SpecialtyPackResolver,
    build_reference_resolver,
)
from decisionmed.specialties import (
    CapabilityRequirement,
    PSYCHIATRY_PACK,
    SpecialtyPackRegistry,
    SpecialtyPackStatus,
    UnknownSpecialtyPackError,
    build_default_specialty_registry,
)


class CapabilityBindingTest(unittest.TestCase):
    def test_binding_is_immutable_and_versioned(self) -> None:
        binding = CapabilityBinding("safety", "test.safety", "1.0.0")

        with self.assertRaises(FrozenInstanceError):
            binding.version = "2.0.0"  # type: ignore[misc]

    def test_binding_rejects_invalid_metadata(self) -> None:
        with self.assertRaisesRegex(ValueError, "canonical lowercase identifier"):
            CapabilityBinding("Safety", "test.safety", "1.0.0")
        with self.assertRaisesRegex(ValueError, "semantic versioning"):
            CapabilityBinding("safety", "test.safety", "v1")


class SpecialtyPackResolverTest(unittest.TestCase):
    def test_psychiatry_loads_as_reference_only_without_execution(self) -> None:
        result = build_reference_resolver().load(
            build_default_specialty_registry(), "psychiatry"
        )

        self.assertEqual(SpecialtyLoadStatus.REFERENCE_ONLY, result.status)
        self.assertEqual(
            PSYCHIATRY_PACK.required_capabilities,
            tuple(binding.capability for binding in result.bindings),
        )
        self.assertEqual((), result.missing_capabilities)
        self.assertEqual((), result.incompatible_capabilities)
        self.assertEqual(("pack_status:reference_only",), result.blocking_reasons)
        self.assertFalse(result.clinical_execution_allowed)
        self.assertEqual(
            "decisionmed.psychiatry:psychiatry:0.1.0", result.trace_id
        )

    def test_missing_capability_blocks_resolution_explicitly(self) -> None:
        resolver = SpecialtyPackResolver(
            (CapabilityBinding("safety", "test.safety", "1.0.0"),)
        )
        pack = replace(
            PSYCHIATRY_PACK,
            key="test-pack",
            capability_requirements=(
                CapabilityRequirement("safety", "1.0.0"),
                CapabilityRequirement("evidence", "1.0.0"),
            ),
        )

        result = resolver.resolve(pack)

        self.assertEqual(SpecialtyLoadStatus.BLOCKED, result.status)
        self.assertEqual(("evidence",), result.missing_capabilities)
        self.assertEqual(("missing_capability:evidence",), result.blocking_reasons)
        self.assertFalse(result.clinical_execution_allowed)

    def test_incompatible_provider_version_blocks_resolution(self) -> None:
        resolver = SpecialtyPackResolver(
            (CapabilityBinding("safety", "test.safety", "2.0.0"),)
        )
        pack = replace(
            PSYCHIATRY_PACK,
            capability_requirements=(
                CapabilityRequirement("safety", "1.0.0"),
            ),
        )

        result = resolver.resolve(pack)

        self.assertEqual(SpecialtyLoadStatus.BLOCKED, result.status)
        self.assertEqual((), result.missing_capabilities)
        self.assertEqual(("safety",), result.incompatible_capabilities)
        self.assertEqual((), result.bindings)
        self.assertEqual(
            ("incompatible_capability:safety:required=1.0.0:found=2.0.0",),
            result.blocking_reasons,
        )

    def test_active_manifest_still_requires_future_clinical_gate(self) -> None:
        pack = replace(PSYCHIATRY_PACK, status=SpecialtyPackStatus.ACTIVE)

        result = build_reference_resolver().resolve(pack)

        self.assertEqual(SpecialtyLoadStatus.READY_FOR_VALIDATION, result.status)
        self.assertEqual(
            ("clinical_activation_gate:not_implemented",), result.blocking_reasons
        )
        self.assertFalse(result.clinical_execution_allowed)

    def test_retired_manifest_is_blocked(self) -> None:
        pack = replace(PSYCHIATRY_PACK, status=SpecialtyPackStatus.RETIRED)

        result = build_reference_resolver().resolve(pack)

        self.assertEqual(SpecialtyLoadStatus.BLOCKED, result.status)
        self.assertEqual(("pack_status:retired",), result.blocking_reasons)

    def test_duplicate_capability_binding_is_rejected(self) -> None:
        binding = CapabilityBinding("safety", "test.safety", "1.0.0")

        with self.assertRaises(DuplicateCapabilityBindingError):
            SpecialtyPackResolver((binding, binding))

    def test_unknown_specialty_remains_an_explicit_error(self) -> None:
        with self.assertRaises(UnknownSpecialtyPackError):
            build_reference_resolver().load(SpecialtyPackRegistry(), "unknown")

    def test_result_schema_contains_no_clinical_output(self) -> None:
        self.assertEqual(
            {
                "pack",
                "status",
                "bindings",
                "missing_capabilities",
                "incompatible_capabilities",
                "blocking_reasons",
                "trace_id",
            },
            {field.name for field in fields(SpecialtyLoadResult)},
        )

    def test_result_rejects_inconsistent_missing_capability_state(self) -> None:
        with self.assertRaisesRegex(ValueError, "require blocked status"):
            SpecialtyLoadResult(
                pack=PSYCHIATRY_PACK,
                status=SpecialtyLoadStatus.REFERENCE_ONLY,
                bindings=(),
                missing_capabilities=("safety",),
                incompatible_capabilities=(),
                blocking_reasons=("pack_status:reference_only",),
                trace_id="test:psychiatry:0.1.0",
            )


if __name__ == "__main__":
    unittest.main()
