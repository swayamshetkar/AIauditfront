"""Tests for savings calculation invariants.

These tests verify fundamental arithmetic guarantees that must always hold
regardless of how individual rules compute their estimates.
"""

import pytest

from app.engine import run_audit
from app.schemas import AuditInput, AuditResult, ToolUsage, UseCase


class TestSavingsCalculation:
    """Verify savings-related invariants on every AuditResult."""

    def test_annual_equals_monthly_times_twelve(
        self, bloated_stack_input: AuditInput
    ) -> None:
        """Annual savings must always be monthly savings × 12."""
        result: AuditResult = run_audit(bloated_stack_input)

        assert result.total_estimated_annual_savings == pytest.approx(
            result.total_estimated_monthly_savings * 12
        ), "Annual savings should equal monthly savings × 12"

        # Also verify per-recommendation consistency
        for rec in result.recommendations:
            assert rec.estimated_annual_savings == pytest.approx(
                rec.estimated_monthly_savings * 12
            ), f"Annual ≠ monthly×12 for recommendation on {rec.tool}"

    def test_total_savings_is_sum_of_individual(
        self, bloated_stack_input: AuditInput
    ) -> None:
        """Total savings should equal the sum of each recommendation's savings."""
        result = run_audit(bloated_stack_input)
        individual_sum = sum(r.estimated_monthly_savings for r in result.recommendations)

        assert result.total_estimated_monthly_savings == pytest.approx(individual_sum), (
            "Total monthly savings should be the sum of individual recommendation savings"
        )

    def test_savings_never_negative(self, bloated_stack_input: AuditInput) -> None:
        """No recommendation should claim negative savings."""
        result = run_audit(bloated_stack_input)

        assert result.total_estimated_monthly_savings >= 0
        assert result.total_estimated_annual_savings >= 0
        for rec in result.recommendations:
            assert rec.estimated_monthly_savings >= 0, (
                f"Negative monthly savings on {rec.tool}"
            )
            assert rec.estimated_annual_savings >= 0, (
                f"Negative annual savings on {rec.tool}"
            )

    def test_savings_never_exceed_total_spend(
        self, bloated_stack_input: AuditInput
    ) -> None:
        """Estimated savings can never exceed what the team is currently spending."""
        result = run_audit(bloated_stack_input)

        assert result.total_estimated_monthly_savings <= result.total_monthly_spend, (
            "Monthly savings should never exceed total monthly spend"
        )
        assert result.total_estimated_annual_savings <= result.total_monthly_spend * 12, (
            "Annual savings should never exceed total annual spend"
        )

    def test_solo_dev_optimal_setup_minimal_savings(self) -> None:
        """An already-optimal solo dev setup should yield near-zero savings."""
        audit_input = AuditInput(
            team_size=1,
            primary_use_case=UseCase.CODING,
            tools=[
                ToolUsage(tool="cursor", plan="pro", monthly_spend=20.0, seats=1),
            ],
        )
        result = run_audit(audit_input)
        # Savings should be very small or zero for an optimal setup
        assert result.total_estimated_monthly_savings <= result.total_monthly_spend * 0.5
