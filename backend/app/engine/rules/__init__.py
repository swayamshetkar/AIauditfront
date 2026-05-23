"""Exports all engine rules."""

from app.engine.rules import (
    api_overspend,
    enterprise_overkill,
    plan_optimization,
    redundancy,
    seat_efficiency,
    workflow_mismatch,
)

ALL_RULES = [
    workflow_mismatch,
    enterprise_overkill,
    redundancy,
    api_overspend,
    seat_efficiency,
    plan_optimization,
]
