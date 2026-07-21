import unittest
from pathlib import Path

from clinical_intelligence import (
    CapabilityLifecycle,
    CapabilityRegistry,
    ClinicalIntelligenceCapability,
    ConfidenceRegistry,
    ContextBroker,
    ContractManager,
    ContractValidator,
    GovernanceGate,
    IntelligenceCoordinator,
    IntelligenceReplay,
    OutputValidator,
    PermissionEngine,
    PolicyRegistry,
)


class ClinicalIntelligenceStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in [
            "coordinator",
            "registry",
            "contracts",
            "context",
            "governance",
            "explainability",
            "audit",
            "models",
        ]:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("clinical_intelligence") / dirname).is_dir())

    def test_registry_lifecycle_contracts_context_and_permissions(self) -> None:
        capability = ClinicalIntelligenceCapability(dependencies=("Clinical Operating Mind",))
        registry = CapabilityRegistry()
        contract = ContractManager().create(capability)
        permission = PermissionEngine().grant(capability, ("Snapshot", "OrderSender"))

        self.assertEqual(registry.register(capability), capability)
        self.assertTrue(CapabilityLifecycle().can_transition("experimental", "registered"))
        self.assertEqual(ContractValidator().validate(contract), ())
        self.assertTrue(ContextBroker().distribute().read_only)
        self.assertEqual(permission.granted, ("Snapshot",))

    def test_governance_explainability_output_and_confidence_are_structural(self) -> None:
        capability = ClinicalIntelligenceCapability()
        permission = PermissionEngine().grant(capability, ("Snapshot",))
        approved = GovernanceGate().evaluate((), permission)
        rejected = GovernanceGate().evaluate(("prescription",), permission)

        self.assertEqual(approved.outcome, "approved_read_only")
        self.assertEqual(rejected.outcome, "rejected")
        self.assertEqual(OutputValidator().validate("trace", ("ref",), ("contract",), "valid"), ())
        self.assertIn("clinical_confidence_scoring:not_available", ConfidenceRegistry().metadata())
        self.assertIn("quality compliance", PolicyRegistry().all())

    def test_coordinator_and_replay_are_non_prescriptive(self) -> None:
        result = IntelligenceCoordinator().evaluate_capability()
        replayed = IntelligenceReplay().replay(result)
        payload = str(result.to_dict()).lower()

        self.assertEqual(result.governance_decision.outcome, "approved_read_only")
        self.assertEqual(result.quality_validation, "valid")
        self.assertTrue(result.read_only_mode)
        self.assertEqual(replayed, result)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("decisao autonoma", payload)


if __name__ == "__main__":
    unittest.main()

