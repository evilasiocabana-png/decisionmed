"""Alert formatting for workspace, audit, logs, and developer views."""

from __future__ import annotations

from safety_engine.models import Alert


class AlertFormatter:
    """Formats alerts for read-only surfaces."""

    def for_workspace(self, alert: Alert) -> dict[str, str]:
        return {
            "id": alert.alert_id,
            "priority": alert.priority,
            "severity": alert.severity,
            "message": alert.message,
        }

    def for_audit(self, alert: Alert) -> dict[str, object]:
        return alert.to_dict()

    def for_log(self, alert: Alert) -> str:
        return f"{alert.priority.upper()} {alert.alert_id}: {alert.message}"

    def for_developer_mode(self, alert: Alert) -> dict[str, object]:
        return {"alert": alert.to_dict(), "trace": alert.trace.to_dict()}
