"""Integration tests for the audit engine.

These tests exercise the full `run_audit` pipeline end-to-end, ensuring that
rules compose correctly, scores are valid, and the output schema is complete.
"""

import pytest

from app.engine import run_audit
from app.schemas import AuditInput, AuditResult, Severity, ToolUsage, UseCase


class TestAuditEngine:
    """End-to-end integration tests against run_audit."""

    def test_bloated_stack_returns_recommendations(
        self, bloated_stack_input: AuditInput
    ) -> None:
        """A heavily over-provisioned stack should produce recommendations and a non-zero score."""
        result: AuditResult = run_audit(bloated_stack_input)

        assert result.overspend_score > 0, "Bloated stack should have a positive overspend score"
        assert len(result.recommendations) > 0, "Expected at least one recommendation"
        assert result.total_monthly_spend > 0
        assert result.tool_count == len(bloated_stack_input.tools)
        assert result.team_size == bloated_stack_input.team_size
        assert result.primary_use_case == bloated_stack_input.primary_use_case

    def test_optimal_setup_low_score(self) -> None:
        """A clean, right-sized setup should yield a low overspend score."""
        audit_input = AuditInput(
            team_size=5,
            primary_use_case=UseCase.CODING,
            tools=[
                ToolUsage(tool="cursor", plan="teams", monthly_spend=200.0, seats=5),
            ],
        )
        result = run_audit(audit_input)

        assert result.overspend_score <= 30, (
            f"Optimal setup should score ≤30, got {result.overspend_score}"
        )

    def test_single_tool_audit(self, cursor_pro_tool: ToolUsage) -> None:
        """Auditing a single tool should work without errors."""
        audit_input = AuditInput(
            team_size=1,
            primary_use_case=UseCase.CODING,
            tools=[cursor_pro_tool],
        )
        result = run_audit(audit_input)

        assert isinstance(result, AuditResult)
        assert result.tool_count == 1
        assert result.tools_analyzed == ["cursor"]
        assert 0 <= result.overspend_score <= 100

    def test_many_tools_does_not_crash(self) -> None:
        """Auditing a large number of tools should complete without errors."""
        tools = [
            ToolUsage(tool="cursor", plan="teams", monthly_spend=200.0, seats=5),
            ToolUsage(tool="github_copilot", plan="enterprise", monthly_spend=195.0, seats=5),
            ToolUsage(tool="windsurf", plan="teams", monthly_spend=200.0, seats=5),
            ToolUsage(tool="chatgpt", plan="business", monthly_spend=125.0, seats=5),
            ToolUsage(tool="claude", plan="team_standard", monthly_spend=125.0, seats=5),
            ToolUsage(tool="gemini", plan="ai_pro", monthly_spend=100.0, seats=5),
            ToolUsage(tool="openai_api", plan="pay_as_you_go", monthly_spend=800.0),
            ToolUsage(tool="anthropic_api", plan="pay_as_you_go", monthly_spend=400.0),
        ]
        audit_input = AuditInput(
            team_size=5,
            primary_use_case=UseCase.CODING,
            tools=tools,
        )
        result = run_audit(audit_input)

        assert isinstance(result, AuditResult)
        assert result.tool_count == len(tools)
        assert 0 <= result.overspend_score <= 100
        assert result.total_monthly_spend > 0

    def test_score_capped_at_100(self, bloated_stack_input: AuditInput) -> None:
        """Overspend score must never exceed 100."""
        result = run_audit(bloated_stack_input)
        assert result.overspend_score <= 100

    def test_score_breakdown_present(self, bloated_stack_input: AuditInput) -> None:
        """Score breakdown should list contributing factors."""
        result = run_audit(bloated_stack_input)
        assert isinstance(result.score_breakdown, list)
        assert result.score_label != ""
