"""Workflow mismatch rule — flags tools being used outside their ideal use case.

Weight: 25 / 100
"""

from __future__ import annotations

from app.schemas import Confidence, Recommendation, Severity, ToolUsage, UseCase
from app.tool_profiles import TOOL_PROFILES

RULE_NAME: str = "workflow_mismatch"
RULE_WEIGHT: int = 25

# Alternative suggestions per mismatch scenario
_WRITING_ALTERNATIVES: dict[str, float] = {"claude": 20.0, "chatgpt": 20.0}
_DATA_ALTERNATIVES: dict[str, float] = {"gemini": 20.0, "chatgpt": 20.0}
_CODING_ALTERNATIVES: dict[str, float] = {"claude": 20.0, "cursor": 20.0}


def _cheapest_alternative(alternatives: dict[str, float]) -> tuple[str, float]:
    """Return (tool_name, price) of the cheapest alternative."""
    name = min(alternatives, key=alternatives.get)  # type: ignore[arg-type]
    return name, alternatives[name]


def evaluate(
    tool: ToolUsage,
    team_size: int,
    primary_use_case: UseCase,
    all_tools: list[ToolUsage],
) -> Recommendation | None:
    """Evaluate whether *tool* is a good workflow fit.

    Returns a :class:`Recommendation` if a mismatch is detected, otherwise
    ``None``.
    """
    profile = TOOL_PROFILES.get(tool.tool.lower())
    if profile is None:
        return None  # unknown tool — nothing to evaluate

    use_case_str = primary_use_case.value
    category = profile.category.value

    # If the tool is ideal for the stated use case → no mismatch
    if use_case_str in profile.ideal_use_cases:
        return None

    # Mixed use case is generally a pass
    if primary_use_case == UseCase.MIXED:
        return None

    # ── Coding tool used for non-coding workflow ────────────────────────
    if category == "coding" and use_case_str in ("writing", "research"):
        alt_name, alt_price = _cheapest_alternative(_WRITING_ALTERNATIVES)
        monthly_savings = max(tool.monthly_spend - alt_price, 0.0)
        return Recommendation(
            tool=tool.tool,
            severity=Severity.HIGH,
            issue=(
                f"{tool.tool.replace('_', ' ').title()} is a coding-focused IDE "
                f"being used by a team primarily focused on {use_case_str}."
            ),
            recommendation=(
                f"Consider switching to {alt_name.replace('_', ' ').title()} "
                f"(~${alt_price:.0f}/mo per seat), which is purpose-built for "
                f"{use_case_str} workflows."
            ),
            reasoning=(
                f"{tool.tool.replace('_', ' ').title()} is optimized for software "
                f"development workflows. For {use_case_str}-focused teams, "
                f"{alt_name.replace('_', ' ').title()} would better serve your needs "
                f"at a lower cost."
            ),
            estimated_monthly_savings=round(monthly_savings, 2),
            estimated_annual_savings=round(monthly_savings * 12, 2),
            confidence=Confidence.HIGH,
        )

    if category == "coding" and use_case_str == "data":
        alt_name, alt_price = _cheapest_alternative(_DATA_ALTERNATIVES)
        monthly_savings = max(tool.monthly_spend - alt_price, 0.0)
        return Recommendation(
            tool=tool.tool,
            severity=Severity.MEDIUM,
            issue=(
                f"{tool.tool.replace('_', ' ').title()} is a code editor being used "
                f"by a data-focused team."
            ),
            recommendation=(
                f"Evaluate {alt_name.replace('_', ' ').title()} or Gemini for data "
                f"analysis workflows that may not require a full IDE."
            ),
            reasoning=(
                f"Data-focused teams typically benefit more from AI assistants with "
                f"strong analytical capabilities than from code-editing IDEs. "
                f"{tool.tool.replace('_', ' ').title()}'s strengths lie in software "
                f"engineering workflows."
            ),
            estimated_monthly_savings=round(monthly_savings, 2),
            estimated_annual_savings=round(monthly_savings * 12, 2),
            confidence=Confidence.MEDIUM,
        )

    # ── Productivity tool used primarily for coding ─────────────────────
    if (
        category == "productivity"
        and use_case_str == "coding"
        and tool.tool.lower() in ("chatgpt", "gemini")
    ):
        alt_name, alt_price = _cheapest_alternative(_CODING_ALTERNATIVES)
        monthly_savings = max(tool.monthly_spend - alt_price, 0.0)
        return Recommendation(
            tool=tool.tool,
            severity=Severity.MEDIUM,
            issue=(
                f"{tool.tool.replace('_', ' ').title()} is being used as the primary "
                f"coding assistant."
            ),
            recommendation=(
                "Consider Claude or a dedicated coding IDE like Cursor for "
                "superior code generation and debugging capabilities."
            ),
            reasoning=(
                f"While {tool.tool.replace('_', ' ').title()} can handle coding "
                f"tasks, Claude and dedicated coding tools provide significantly "
                f"better code quality, multi-file awareness, and IDE integration."
            ),
            estimated_monthly_savings=round(monthly_savings, 2),
            estimated_annual_savings=round(monthly_savings * 12, 2),
            confidence=Confidence.MEDIUM,
        )

    return None
