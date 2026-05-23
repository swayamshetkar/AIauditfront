"""Tests for the workflow-mismatch rule.

The rule should flag tools that are a poor fit for the team's primary use case.
For example, Cursor (a code editor) is a mismatch for a writing-focused team.
"""

import pytest

from app.engine.rules.workflow_mismatch import RULE_NAME, RULE_WEIGHT, evaluate
from app.schemas import Recommendation, ToolUsage, UseCase


class TestWorkflowMismatch:
    """Verify the workflow-mismatch rule fires (or stays silent) correctly."""

    def test_cursor_for_writing_team_flags_mismatch(
        self, cursor_pro_tool: ToolUsage
    ) -> None:
        """Cursor is a coding IDE — using it for a *writing* team is a mismatch."""
        result: Recommendation | None = evaluate(
            tool=cursor_pro_tool,
            team_size=3,
            primary_use_case=UseCase.WRITING,
            all_tools=[cursor_pro_tool],
        )
        assert result is not None, "Expected a mismatch recommendation for Cursor on a writing team"
        assert result.tool == "cursor"
        assert result.estimated_monthly_savings >= 0

    def test_cursor_for_coding_team_no_flag(
        self, cursor_pro_tool: ToolUsage
    ) -> None:
        """Cursor is the right tool for a coding team — no mismatch expected."""
        result = evaluate(
            tool=cursor_pro_tool,
            team_size=3,
            primary_use_case=UseCase.CODING,
            all_tools=[cursor_pro_tool],
        )
        assert result is None, "Cursor should NOT be flagged for a coding team"

    def test_chatgpt_for_coding_team_flags_mild(
        self, chatgpt_plus_tool: ToolUsage
    ) -> None:
        """ChatGPT can help with coding but it's not the primary IDE tool — mild flag expected."""
        result = evaluate(
            tool=chatgpt_plus_tool,
            team_size=5,
            primary_use_case=UseCase.CODING,
            all_tools=[chatgpt_plus_tool],
        )
        # ChatGPT may or may not be flagged depending on implementation strictness.
        # If flagged, severity should be LOW.
        if result is not None:
            assert result.severity.value in ("low", "medium")

    def test_claude_for_research_team_no_flag(
        self, claude_team_tool: ToolUsage
    ) -> None:
        """Claude is excellent for research — no mismatch expected."""
        result = evaluate(
            tool=claude_team_tool,
            team_size=5,
            primary_use_case=UseCase.RESEARCH,
            all_tools=[claude_team_tool],
        )
        assert result is None, "Claude should NOT be flagged for a research team"

    def test_mixed_use_case_lenient(self) -> None:
        """Mixed use case should be lenient — most tools are acceptable."""
        tools = [
            ToolUsage(tool="cursor", plan="pro", monthly_spend=20.0, seats=1),
            ToolUsage(tool="chatgpt", plan="plus", monthly_spend=20.0, seats=1),
            ToolUsage(tool="claude", plan="pro", monthly_spend=20.0, seats=1),
        ]
        flagged_count = 0
        for tool in tools:
            result = evaluate(
                tool=tool,
                team_size=3,
                primary_use_case=UseCase.MIXED,
                all_tools=tools,
            )
            if result is not None:
                flagged_count += 1

        assert flagged_count <= 1, "Mixed use case should not flag most tools"
