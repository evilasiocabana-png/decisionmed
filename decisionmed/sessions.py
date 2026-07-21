"""In-memory workflow session orchestration without patient content."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from threading import RLock
from uuid import uuid4

from .audit import AuditLedger, AuditRecord
from .domain import DomainEvent
from .specialties import SpecialtyPackRegistry, UnknownSpecialtyPackError
from .workflows import UnknownWorkflowError, WorkflowRegistry


class WorkflowSessionError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class WorkflowSessionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


@dataclass(frozen=True, slots=True)
class WorkflowSession:
    """Structural progress only; contains no clinical or free-text data."""

    session_id: str
    trace_id: str
    specialty_key: str
    workflow_id: str
    step_keys: tuple[str, ...]
    current_position: int = 0
    completed_step_keys: tuple[str, ...] = ()
    status: WorkflowSessionStatus = WorkflowSessionStatus.ACTIVE

    def __post_init__(self) -> None:
        for field_name in ("session_id", "trace_id", "specialty_key", "workflow_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise WorkflowSessionError(
                    f"workflow_session.{field_name}", f"{field_name} cannot be empty"
                )
        steps = tuple(self.step_keys)
        completed = tuple(self.completed_step_keys)
        if not steps or len(set(steps)) != len(steps):
            raise WorkflowSessionError(
                "workflow_session.step_keys", "step keys must be non-empty and unique"
            )
        if not 0 <= self.current_position <= len(steps):
            raise WorkflowSessionError(
                "workflow_session.position", "current position is outside the workflow"
            )
        if completed != steps[: self.current_position]:
            raise WorkflowSessionError(
                "workflow_session.completed_steps",
                "completed steps must be the ordered workflow prefix",
            )
        expected_status = (
            WorkflowSessionStatus.COMPLETED
            if self.current_position == len(steps)
            else WorkflowSessionStatus.ACTIVE
        )
        if self.status is not expected_status:
            raise WorkflowSessionError(
                "workflow_session.status", "status does not match progress"
            )
        object.__setattr__(self, "step_keys", steps)
        object.__setattr__(self, "completed_step_keys", completed)

    @property
    def current_step_key(self) -> str | None:
        if self.status is WorkflowSessionStatus.COMPLETED:
            return None
        return self.step_keys[self.current_position]

    @property
    def clinical_execution_allowed(self) -> bool:
        return False

    def to_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "trace_id": self.trace_id,
            "specialty_key": self.specialty_key,
            "workflow_id": self.workflow_id,
            "status": self.status.value,
            "current_position": self.current_position,
            "current_step_key": self.current_step_key,
            "completed_step_keys": list(self.completed_step_keys),
            "total_steps": len(self.step_keys),
            "clinical_execution_allowed": False,
        }


class WorkflowSessionService:
    """Advance manifest steps in order and append metadata-only audit events."""

    def __init__(
        self,
        specialties: SpecialtyPackRegistry,
        workflows: WorkflowRegistry,
        audit: AuditLedger | None = None,
        max_sessions: int = 1000,
    ) -> None:
        if not isinstance(specialties, SpecialtyPackRegistry):
            raise TypeError("specialties must be a SpecialtyPackRegistry")
        if not isinstance(workflows, WorkflowRegistry):
            raise TypeError("workflows must be a WorkflowRegistry")
        if (
            not isinstance(max_sessions, int)
            or isinstance(max_sessions, bool)
            or max_sessions < 1
        ):
            raise ValueError("max_sessions must be a positive integer")
        self._specialties = specialties
        self._workflows = workflows
        self._audit = audit or AuditLedger()
        self._max_sessions = max_sessions
        self._sessions: dict[str, WorkflowSession] = {}
        self._lock = RLock()

    def start(self, specialty_key: str) -> WorkflowSession:
        with self._lock:
            if len(self._sessions) >= self._max_sessions:
                raise WorkflowSessionError(
                    "workflow_session.capacity", "in-memory session capacity reached"
                )
            try:
                self._specialties.require(specialty_key)
                workflow = self._workflows.require(specialty_key)
            except (UnknownSpecialtyPackError, UnknownWorkflowError) as exc:
                raise WorkflowSessionError(
                    "workflow_session.unknown_specialty",
                    f"workflow not available: {specialty_key}",
                ) from exc

            session_id = str(uuid4())
            trace_id = f"workflow-session:{session_id}"
            session = WorkflowSession(
                session_id=session_id,
                trace_id=trace_id,
                specialty_key=specialty_key,
                workflow_id=workflow.workflow_id,
                step_keys=tuple(step.key for step in workflow.steps),
            )
            self._sessions[session_id] = session
            self._record(
                session,
                "workflow.session-started",
                (("specialty", specialty_key), ("workflow", workflow.workflow_id)),
            )
            return session

    def get(self, session_id: str) -> WorkflowSession:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                raise WorkflowSessionError(
                    "workflow_session.unknown", f"session not found: {session_id}"
                )
            return session

    def advance(self, session_id: str, step_key: str) -> WorkflowSession:
        with self._lock:
            session = self.get(session_id)
            if session.status is WorkflowSessionStatus.COMPLETED:
                raise WorkflowSessionError(
                    "workflow_session.completed", "completed session cannot advance"
                )
            if step_key != session.current_step_key:
                raise WorkflowSessionError(
                    "workflow_session.out_of_order",
                    f"expected step: {session.current_step_key}",
                )

            next_position = session.current_position + 1
            next_status = (
                WorkflowSessionStatus.COMPLETED
                if next_position == len(session.step_keys)
                else WorkflowSessionStatus.ACTIVE
            )
            updated = replace(
                session,
                current_position=next_position,
                completed_step_keys=session.step_keys[:next_position],
                status=next_status,
            )
            self._sessions[session_id] = updated
            event_name = (
                "workflow.session-completed"
                if next_status is WorkflowSessionStatus.COMPLETED
                else "workflow.step-completed"
            )
            self._record(
                updated,
                event_name,
                (("step", step_key), ("position", str(next_position))),
            )
            return updated

    def audit_records(self, session_id: str) -> tuple[AuditRecord, ...]:
        with self._lock:
            self.get(session_id)
            return tuple(
                record
                for record in self._audit.records()
                if record.aggregate_id == session_id
            )

    @property
    def audit_integrity_valid(self) -> bool:
        with self._lock:
            return self._audit.verify()

    def _record(
        self,
        session: WorkflowSession,
        event_name: str,
        payload: tuple[tuple[str, str], ...],
    ) -> None:
        self._audit.append(
            DomainEvent(event_name, session.session_id, payload), session.trace_id
        )
