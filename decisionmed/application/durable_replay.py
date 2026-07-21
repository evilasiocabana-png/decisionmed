"""Durable, process-shared replay protection for authority decisions."""

from __future__ import annotations

from pathlib import Path
import sqlite3
from threading import Lock


class SQLiteAuthorityDecisionReplayGuard:
    """Atomically reserve authority decisions in a local SQLite database.

    The namespace keeps independent authority workflows from colliding while the
    unique database constraint protects across service instances and restarts.
    This guard supplies replay protection only; it never grants authority.
    """

    def __init__(self, database_path: Path, *, namespace: str) -> None:
        if not isinstance(database_path, Path):
            raise TypeError("database_path must be a Path")
        if not database_path.parent.is_dir():
            raise ValueError("database parent directory must exist")
        if not isinstance(namespace, str) or not namespace.strip():
            raise ValueError("namespace must be a non-empty string")
        self._database_path = database_path
        self._namespace = namespace
        self._lock = Lock()
        self._initialize()

    def reserve(self, *, authority_provider: str, decision_reference: str) -> bool:
        if not isinstance(authority_provider, str) or not authority_provider:
            raise ValueError("authority_provider must be a non-empty string")
        if not isinstance(decision_reference, str) or not decision_reference:
            raise ValueError("decision_reference must be a non-empty string")
        with self._lock:
            connection = self._connection()
            try:
                with connection:
                    result = connection.execute(
                        """
                        INSERT INTO authority_decision_replays
                            (namespace, authority_provider, decision_reference)
                        VALUES (?, ?, ?)
                        ON CONFLICT(namespace, authority_provider, decision_reference)
                        DO NOTHING
                        """,
                        (self._namespace, authority_provider, decision_reference),
                    )
                    return result.rowcount == 1
            finally:
                connection.close()

    def _initialize(self) -> None:
        with self._lock:
            connection = self._connection()
            try:
                with connection:
                    connection.execute(
                        """
                        CREATE TABLE IF NOT EXISTS authority_decision_replays (
                            namespace TEXT NOT NULL,
                            authority_provider TEXT NOT NULL,
                            decision_reference TEXT NOT NULL,
                            PRIMARY KEY (namespace, authority_provider, decision_reference)
                        )
                        """
                    )
            finally:
                connection.close()

    def _connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path, timeout=5)
        connection.execute("PRAGMA journal_mode=WAL")
        return connection
