"""Tests for the API overspend rule.

The rule should flag teams whose per-developer API spend is unreasonably high
relative to team size and typical consumption patterns.
"""

import pytest

from app.engine.rules.api_overspend import RULE_NAME, RULE_WEIGHT, evaluate
from app.schemas import Recommendation, Severity, ToolUsage, UseCase


class TestAPIOverspend:
    """Verify API-overspend detection across different spend / team-size combos."""

    def test_small_team_high_api_spend_flags(self) -> None:
        """3 devs spending $2 000/mo on OpenAI API → should flag high overspend."""
        tool = ToolUsage(
            tool="openai_api", plan="pay_as_you_go", monthly_spend=2000.0
        )
        result: Recommendation | None = evaluate(
            tool=tool,
            team_size=3,
            primary_use_case=UseCase.CODING,
            all_tools=[tool],
        )
        assert result is not None, "Expected overspend flag for $2 000/mo API on 3-dev team"
        assert result.tool == "openai_api"
        assert result.severity in (Severity.HIGH, Severity.MEDIUM)
        assert result.estimated_monthly_savings > 0

    def test_large_team_moderate_spend_no_flag(self) -> None:
        """50 devs spending $1 000/mo on API → $20/dev/mo is reasonable."""
        tool = ToolUsage(
            tool="openai_api", plan="pay_as_you_go", monthly_spend=1000.0
        )
        result = evaluate(
            tool=tool,
            team_size=50,
            primary_use_case=UseCase.CODING,
            all_tools=[tool],
        )
        assert result is None, "50-dev team at $1 000/mo should NOT be flagged"

    def test_solo_dev_low_spend_no_flag(self) -> None:
        """Solo dev spending $40/mo on Anthropic API → perfectly reasonable."""
        tool = ToolUsage(
            tool="anthropic_api", plan="pay_as_you_go", monthly_spend=40.0
        )
        result = evaluate(
            tool=tool,
            team_size=1,
            primary_use_case=UseCase.CODING,
            all_tools=[tool],
        )
        assert result is None, "Solo dev at $50/mo on Anthropic API should NOT be flagged"
