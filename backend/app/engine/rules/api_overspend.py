"""API overspend rule — estimates expected API spend and compares to actual.

Weight: 35 / 100
"""

from __future__ import annotations

from app.schemas import Confidence, Recommendation, Severity, ToolUsage, UseCase
from app.tool_profiles import TOOL_PROFILES
from app.pricing.registry import PRICING_REGISTRY

RULE_NAME: str = "api_overspend"
RULE_WEIGHT: int = 35

# Workflow multipliers — how much AI usage a given workflow pattern drives
_WORKFLOW_MULTIPLIERS: dict[str, float] = {
    "coding": 1.4,
    "writing": 0.8,
    "research": 1.2,
    "data": 1.5,
    "mixed": 1.0,
}

# Base rate per developer per month for moderate API usage (USD)
_BASE_RATE_PER_DEV: float = 15.0

# Severity thresholds (actual / expected ratio)
_HIGH_THRESHOLD: float = 2.0
_MEDIUM_THRESHOLD: float = 1.5
_LOW_THRESHOLD: float = 1.2


def _is_usage_based(tool: ToolUsage) -> bool:
    """Return True if the tool has usage-based pricing components."""
    profile = TOOL_PROFILES.get(tool.tool.lower())
    if profile is not None:
        return profile.pricing_type.value in ("usage", "seat+api")
    # Fallback: check if the plan is pay-as-you-go or if we know it's an API tool
    tool_plans = PRICING_REGISTRY.get(tool.tool.lower(), {})
    plan_data = tool_plans.get(tool.plan.lower(), {})
    return plan_data.get("monthly") is None and tool.monthly_spend > 0


def _get_token_intensity(tool: ToolUsage) -> float:
    """Return token intensity factor for the tool."""
    profile = TOOL_PROFILES.get(tool.tool.lower())
    if profile is not None:
        return profile.token_intensity
    return 1.0  # default


def _format_tool(name: str) -> str:
    return name.replace("_", " ").title()


def evaluate(
    tool: ToolUsage,
    team_size: int,
    primary_use_case: UseCase,
    all_tools: list[ToolUsage],
) -> Recommendation | None:
    """Flag API tools where actual spend significantly exceeds expected."""
    if not _is_usage_based(tool):
        return None

    workflow_multiplier = _WORKFLOW_MULTIPLIERS.get(primary_use_case.value, 1.0)
    token_intensity = _get_token_intensity(tool)

    estimated_usage = team_size * workflow_multiplier * token_intensity
    expected_monthly = estimated_usage * _BASE_RATE_PER_DEV
    actual_spend = tool.monthly_spend

    if expected_monthly <= 0:
        return None

    ratio = actual_spend / expected_monthly
    tool_label = _format_tool(tool.tool)

    if ratio >= _HIGH_THRESHOLD:
        severity = Severity.HIGH
        confidence = Confidence.HIGH
        monthly_savings = round(actual_spend - expected_monthly, 2)
    elif ratio >= _MEDIUM_THRESHOLD:
        severity = Severity.MEDIUM
        confidence = Confidence.MEDIUM
        monthly_savings = round(actual_spend - expected_monthly, 2)
    elif ratio >= _LOW_THRESHOLD:
        severity = Severity.LOW
        confidence = Confidence.LOW
        monthly_savings = round(actual_spend - expected_monthly, 2)
    else:
        return None  # spending within expected range

    return Recommendation(
        tool=tool.tool,
        severity=severity,
        issue=(
            f"{tool_label} API spend of ${actual_spend:,.0f}/mo is "
            f"{ratio:.1f}x the expected spend of ${expected_monthly:,.0f}/mo "
            f"for a {primary_use_case.value} team of {team_size}."
        ),
        recommendation=(
            f"Review API usage patterns and implement cost controls. "
            f"Consider setting budget alerts, optimizing prompt lengths, "
            f"caching frequent queries, or switching to more cost-effective "
            f"models for routine tasks."
        ),
        reasoning=(
            f"Based on team size ({team_size}), workflow type "
            f"({primary_use_case.value}), and typical {tool_label} usage "
            f"intensity, the expected monthly spend is approximately "
            f"${expected_monthly:,.0f}. Your actual spend significantly "
            f"exceeds this benchmark, suggesting potential inefficiencies "
            f"in API usage patterns."
        ),
        estimated_monthly_savings=max(monthly_savings, 0.0),
        estimated_annual_savings=max(round(monthly_savings * 12, 2), 0.0),
        confidence=confidence,
    )
