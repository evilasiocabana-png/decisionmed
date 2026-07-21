import inspect
from concurrent.futures import ThreadPoolExecutor
import unittest

from decisionmed.sessions import (
    WorkflowSessionError,
    WorkflowSessionService,
    WorkflowSessionStatus,
)
from decisionmed.specialties import build_default_specialty_registry
from decisionmed.workflows import build_default_workflow_registry


def service() -> WorkflowSessionService:
    specialties = build_default_specialty_registry()
    return WorkflowSessionService(
        specialties, build_default_workflow_registry(specialties)
    )


class WorkflowSessionServiceTest(unittest.TestCase):
    def test_start_records_only_structural_state_and_audit_metadata(self) -> None:
        sessions = service()
        session = sessions.start("cardiology")

        self.assertEqual(WorkflowSessionStatus.ACTIVE, session.status)
        self.assertEqual("context", session.current_step_key)
        self.assertEqual(7, len(session.step_keys))
        self.assertFalse(session.clinical_execution_allowed)
        self.assertTrue(sessions.audit_integrity_valid)
        self.assertEqual(1, len(sessions.audit_records(session.session_id)))

    def test_advance_is_strictly_ordered(self) -> None:
        sessions = service()
        session = sessions.start("cardiology")

        with self.assertRaises(WorkflowSessionError) as out_of_order:
            sessions.advance(session.session_id, "risk")
        self.assertEqual("workflow_session.out_of_order", out_of_order.exception.code)

        advanced = sessions.advance(session.session_id, "context")
        self.assertEqual("risk", advanced.current_step_key)
        self.assertEqual(("context",), advanced.completed_step_keys)

    def test_complete_session_remains_non_clinical_and_auditable(self) -> None:
        sessions = service()
        session = sessions.start("psychiatry")
        for step_key in session.step_keys:
            session = sessions.advance(session.session_id, step_key)

        self.assertEqual(WorkflowSessionStatus.COMPLETED, session.status)
        self.assertIsNone(session.current_step_key)
        self.assertFalse(session.clinical_execution_allowed)
        self.assertEqual(14, len(sessions.audit_records(session.session_id)))
        self.assertTrue(sessions.audit_integrity_valid)
        with self.assertRaises(WorkflowSessionError):
            sessions.advance(session.session_id, "monitoring")

    def test_unknown_specialty_and_session_fail_closed(self) -> None:
        sessions = service()
        with self.assertRaises(WorkflowSessionError) as specialty:
            sessions.start("dermatology")
        with self.assertRaises(WorkflowSessionError) as session:
            sessions.get("missing")

        self.assertEqual("workflow_session.unknown_specialty", specialty.exception.code)
        self.assertEqual("workflow_session.unknown", session.exception.code)

    def test_sessions_are_isolated(self) -> None:
        sessions = service()
        first = sessions.start("neurology")
        second = sessions.start("neurology")
        sessions.advance(first.session_id, first.current_step_key or "")

        self.assertNotEqual(first.session_id, second.session_id)
        self.assertEqual(0, sessions.get(second.session_id).current_position)

    def test_in_memory_capacity_is_bounded(self) -> None:
        specialties = build_default_specialty_registry()
        sessions = WorkflowSessionService(
            specialties,
            build_default_workflow_registry(specialties),
            max_sessions=1,
        )
        sessions.start("cardiology")

        with self.assertRaises(WorkflowSessionError) as capacity:
            sessions.start("neurology")
        self.assertEqual("workflow_session.capacity", capacity.exception.code)

    def test_concurrent_starts_keep_unique_sessions_and_valid_audit(self) -> None:
        sessions = service()
        with ThreadPoolExecutor(max_workers=8) as executor:
            created = tuple(executor.map(sessions.start, ("cardiology",) * 20))

        self.assertEqual(20, len({item.session_id for item in created}))
        self.assertTrue(sessions.audit_integrity_valid)

    def test_mutation_api_accepts_no_patient_or_free_text_content(self) -> None:
        parameters = set(inspect.signature(WorkflowSessionService.advance).parameters)

        self.assertEqual({"self", "session_id", "step_key"}, parameters)


if __name__ == "__main__":
    unittest.main()
