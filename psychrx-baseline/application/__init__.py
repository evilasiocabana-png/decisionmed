"""Application layer for PsychRx.

This package exposes use-case oriented contracts for interfaces. It must not
contain primary clinical rules, prescribing behavior, or scientific evidence.
"""

__all__ = [
    "app_service",
    "app_view_model",
    "clinical_decision_support_contract",
    "clinical_decision_support_service",
    "decision_support_rule_table",
    "specialized_gpt_decision_support_adapter",
]
