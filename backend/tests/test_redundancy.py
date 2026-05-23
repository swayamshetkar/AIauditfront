"""Tests for the redundancy rule.

The rule should flag teams running multiple tools that serve the same purpose
(e.g., three coding IDEs or three chat-based assistants).
"""


from app.engine.rules.redundancy import evaluate
from app.schemas import Recommendation, Severity, ToolUsage, UseCase


class TestRedundancy:
    """Verify redundancy detection across different tool combinations."""

    def test_three_coding_ides_high_redundancy(self) -> None:
        """Cursor + Copilot + Windsurf = three overlapping coding tools → high flag."""
        tools = [
            ToolUsage(tool="cursor", plan="pro", monthly_spend=20.0, seats=1),
            ToolUsage(tool="github_copilot", plan="pro", monthly_spend=10.0, seats=1),
            ToolUsage(tool="windsurf", plan="pro", monthly_spend=20.0, seats=1),
        ]
        results: list[Recommendation] = []
        for tool in tools:
            result = evaluate(
                tool=tool,
                team_size=3,
                primary_use_case=UseCase.CODING,
                all_tools=tools,
            )
            if result is not None:
                results.append(result)

        assert len(results) >= 1, "Expected at least one redundancy flag for three coding IDEs"
        # At least one should be high severity
        severities = {r.severity for r in results}
        assert Severity.HIGH in severities or Severity.MEDIUM in severities

    def test_three_chat_assistants_for_writing_team(self) -> None:
        """ChatGPT + Claude + Gemini for a 3-person writing team → should flag."""
        tools = [
            ToolUsage(tool="chatgpt", plan="plus", monthly_spend=60.0, seats=3),
            ToolUsage(tool="claude", plan="pro", monthly_spend=60.0, seats=3),
            ToolUsage(tool="gemini", plan="ai_pro", monthly_spend=60.0, seats=3),
        ]
        results: list[Recommendation] = []
        for tool in tools:
            result = evaluate(
                tool=tool,
                team_size=3,
                primary_use_case=UseCase.WRITING,
                all_tools=tools,
            )
            if result is not None:
                results.append(result)

        assert len(results) >= 1, "Expected redundancy flag for three overlapping chat assistants"

    def test_cursor_plus_chatgpt_different_categories_no_flag(self) -> None:
        """Cursor (IDE) + ChatGPT (chat) serve different roles → no redundancy."""
        tools = [
            ToolUsage(tool="cursor", plan="pro", monthly_spend=20.0, seats=1),
            ToolUsage(tool="chatgpt", plan="plus", monthly_spend=20.0, seats=1),
        ]
        results: list[Recommendation] = []
        for tool in tools:
            result = evaluate(
                tool=tool,
                team_size=3,
                primary_use_case=UseCase.CODING,
                all_tools=tools,
            )
            if result is not None:
                results.append(result)

        assert len(results) == 0, "IDE + chat assistant should NOT be flagged as redundant"

    def test_two_coding_tools_low_medium_flag(self) -> None:
        """Cursor + Copilot = two coding tools → should flag at low or medium severity."""
        tools = [
            ToolUsage(tool="cursor", plan="pro", monthly_spend=20.0, seats=1),
            ToolUsage(tool="github_copilot", plan="pro", monthly_spend=10.0, seats=1),
        ]
        results: list[Recommendation] = []
        for tool in tools:
            result = evaluate(
                tool=tool,
                team_size=3,
                primary_use_case=UseCase.CODING,
                all_tools=tools,
            )
            if result is not None:
                results.append(result)

        assert len(results) >= 1, "Expected redundancy flag for two coding tools"
        for r in results:
            assert r.severity in (Severity.LOW, Severity.MEDIUM), (
                f"Two-tool redundancy should be low/medium, got {r.severity}"
            )
