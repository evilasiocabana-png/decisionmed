from dataclasses import replace
import unittest

from decisionmed.audit import AuditError, AuditLedger, verify_chain
from decisionmed.domain import DomainEvent


def event(name: str, event_id: str) -> DomainEvent:
    return DomainEvent(
        name=name,
        aggregate_id="session.synthetic",
        payload=(("specialty", "cardiology"),),
        event_id=event_id,
    )


class AuditLedgerTest(unittest.TestCase):
    def test_append_builds_ordered_verifiable_hash_chain(self) -> None:
        ledger = AuditLedger()
        first = ledger.append(event("workflow.started", "event-1"), "trace.run")
        second = ledger.append(event("workflow.advanced", "event-2"), "trace.run")

        self.assertEqual(1, first.sequence)
        self.assertEqual(first.record_hash, second.previous_hash)
        self.assertTrue(ledger.verify())
        self.assertEqual((first, second), ledger.records())

    def test_tampered_content_or_hash_is_detected(self) -> None:
        ledger = AuditLedger()
        ledger.append(event("workflow.started", "event-1"), "trace.run")
        second = ledger.append(event("workflow.advanced", "event-2"), "trace.run")
        tampered = (*ledger.records()[:1], replace(second, record_hash="f" * 64))

        self.assertFalse(verify_chain(tampered))

    def test_records_and_collection_are_immutable_to_callers(self) -> None:
        ledger = AuditLedger()
        record = ledger.append(event("workflow.started", "event-1"), "trace.run")

        with self.assertRaises(AttributeError):
            record.trace_id = "changed"  # type: ignore[misc]
        self.assertIsInstance(ledger.records(), tuple)

    def test_duplicate_event_is_rejected(self) -> None:
        ledger = AuditLedger()
        item = event("workflow.started", "event-1")
        ledger.append(item, "trace.run")

        with self.assertRaises(AuditError) as duplicate:
            ledger.append(item, "trace.run")
        self.assertEqual("audit.duplicate_event", duplicate.exception.code)

    def test_metadata_is_bounded_and_canonical(self) -> None:
        ledger = AuditLedger()
        invalid_key = DomainEvent(
            "workflow.started", "session.synthetic", (("Invalid Key", "value"),)
        )
        excessive_value = DomainEvent(
            "workflow.started", "session.synthetic", (("key", "x" * 201),)
        )

        with self.assertRaises(AuditError):
            ledger.append(invalid_key, "trace.run")
        with self.assertRaises(AuditError):
            ledger.append(excessive_value, "trace.run")

    def test_empty_chain_is_valid(self) -> None:
        self.assertTrue(verify_chain(()))


if __name__ == "__main__":
    unittest.main()
