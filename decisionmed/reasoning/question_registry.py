"""Identity-only registry for future Question Engine implementations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import re

from .gate import ReasoningError
from .question_engine import QuestionEngine


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


@dataclass(frozen=True, slots=True)
class QuestionEngineBinding:
    """Approved structural identity; it contains no clinical behavior."""

    engine_id: str
    provider: str
    contract_version: str

    def __post_init__(self) -> None:
        for field_name in ("engine_id", "provider"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
                _fail(field_name, f"{field_name} must be canonical")
        if not isinstance(self.contract_version, str) or not _VERSION.fullmatch(
            self.contract_version
        ):
            _fail("contract_version", "contract version must use semantic versioning")

    @property
    def engine_invocation_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


class QuestionEngineRegistry:
    """Bind ports to approved identities without invoking their implementations."""

    def __init__(
        self,
        bindings: Iterable[QuestionEngineBinding],
        engines: Iterable[QuestionEngine] = (),
    ) -> None:
        values = tuple(bindings)
        if not values or not all(isinstance(item, QuestionEngineBinding) for item in values):
            _fail("bindings", "at least one valid engine binding is required")
        if len({item.engine_id for item in values}) != len(values):
            _fail("bindings", "engine bindings must have unique ids")
        self._bindings = {item.engine_id: item for item in values}
        self._engines: dict[str, QuestionEngine] = {}
        for engine in engines:
            self.register(engine)

    def register(self, engine: QuestionEngine) -> QuestionEngine:
        if not isinstance(engine, QuestionEngine):
            raise TypeError("engine must satisfy the QuestionEngine protocol")
        binding = self._bindings.get(engine.engine_id)
        if binding is None:
            _fail("unknown_binding", f"binding not registered: {engine.engine_id}")
        if (
            engine.provider != binding.provider
            or engine.contract_version != binding.contract_version
        ):
            _fail("identity_mismatch", "engine identity must exactly match its binding")
        if engine.engine_id in self._engines:
            _fail("duplicate", f"engine already registered: {engine.engine_id}")
        self._engines[engine.engine_id] = engine
        return engine

    def get(self, engine_id: str) -> QuestionEngine | None:
        return self._engines.get(engine_id)

    def all(self) -> tuple[QuestionEngine, ...]:
        return tuple(self._engines[key] for key in sorted(self._engines))

    @property
    def bindings(self) -> tuple[QuestionEngineBinding, ...]:
        return tuple(self._bindings[key] for key in sorted(self._bindings))

    @property
    def missing_engine_ids(self) -> tuple[str, ...]:
        return tuple(
            engine_id
            for engine_id in sorted(self._bindings)
            if engine_id not in self._engines
        )

    @property
    def complete(self) -> bool:
        return not self.missing_engine_ids

    @property
    def engine_invocation_allowed(self) -> bool:
        return False

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


def _fail(field_name: str, message: str) -> None:
    raise ReasoningError(f"question_engine_registry.{field_name}", message)
