"""Tests for the enterprise-overkill rule.

The rule should flag teams on expensive enterprise plans when a cheaper tier
would serve them just as well given their team size.
"""


from app.engine.rules.enterprise_overkill import evaluate
from app.schemas import Recommendation, ToolUsage, UseCase


class TestEnterpriseOverkill:
    """Verify enterprise-overkill detection across plan / team-size combos."""

    def test_small_team_copilot_enterprise_flags(
        self, copilot_enterprise_tool: ToolUsage
    ) -> None:
        """3-person team on Copilot Enterprise ($39/seat) → recommend Business ($19/seat)."""
        result: Recommendation | None = evaluate(
            tool=copilot_enterprise_tool,
            team_size=3,
            primary_use_case=UseCase.CODING,
            all_tools=[copilot_enterprise_tool],
        )
        assert result is not None, "Expected overkill flag for 3-person team on Copilot Enterprise"
        assert result.tool == "github_copilot"
        assert result.estimated_monthly_savings > 0
        assert "business" in result.recommendation.lower() or "pro" in result.recommendation.lower()

    def test_solo_dev_chatgpt_business_flags(self) -> None:
        """Solo developer on ChatGPT Business ($25/seat) → recommend Plus ($20)."""
        tool = ToolUsage(tool="chatgpt", plan="business", monthly_spend=25.0, seats=1)
        result = evaluate(
            tool=tool,
            team_size=1,
            primary_use_case=UseCase.CODING,
            all_tools=[tool],
        )
        assert result is not None, "Expected overkill flag for solo dev on ChatGPT Business"
        assert result.tool == "chatgpt"
        assert result.estimated_monthly_savings > 0

    def test_large_team_enterprise_no_flag(self) -> None:
        """50-person team on Copilot Enterprise → enterprise plan is justified."""
        tool = ToolUsage(
            tool="github_copilot", plan="enterprise", monthly_spend=1950.0, seats=50
        )
        result = evaluate(
            tool=tool,
            team_size=50,
            primary_use_case=UseCase.CODING,
            all_tools=[tool],
        )
        assert result is None, "50-person team should NOT be flagged for enterprise plan"

    def test_small_team_claude_team_flags(
        self, claude_team_tool: ToolUsage
    ) -> None:
        """2-person team on Claude Team → flag overkill (team plan min is 5 seats)."""
        result = evaluate(
            tool=claude_team_tool,
            team_size=2,
            primary_use_case=UseCase.RESEARCH,
            all_tools=[claude_team_tool],
        )
        assert result is not None, "Expected overkill flag for 2-person team on Claude Team"
        assert result.tool == "claude"
        assert result.estimated_monthly_savings > 0
