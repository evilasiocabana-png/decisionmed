from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from decisionmed.application import SQLiteAuthorityDecisionReplayGuard


class SQLiteAuthorityDecisionReplayGuardTest(unittest.TestCase):
    def test_reservation_survives_a_new_guard_instance(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "authority-replays.sqlite3"
            first = SQLiteAuthorityDecisionReplayGuard(
                path, namespace="question-engine"
            )
            second = SQLiteAuthorityDecisionReplayGuard(
                path, namespace="question-engine"
            )

            self.assertTrue(
                first.reserve(
                    authority_provider="reviewer.synthetic",
                    decision_reference="decision-1",
                )
            )
            self.assertFalse(
                second.reserve(
                    authority_provider="reviewer.synthetic",
                    decision_reference="decision-1",
                )
            )

    def test_namespaces_are_isolated(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "authority-replays.sqlite3"
            question = SQLiteAuthorityDecisionReplayGuard(
                path, namespace="question-engine"
            )
            safety = SQLiteAuthorityDecisionReplayGuard(path, namespace="safety-review")

            self.assertTrue(
                question.reserve(authority_provider="provider", decision_reference="1")
            )
            self.assertTrue(
                safety.reserve(authority_provider="provider", decision_reference="1")
            )
