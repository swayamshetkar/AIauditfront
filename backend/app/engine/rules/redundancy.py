"""Redundancy rule — detects overlapping tools in the same category.

Weight: 20 / 100
"""

from __future__ import annotations

from collections import defaultdict

from app.schemas import Confidence, Recommendation, Severity, ToolUsage, UseCase
from app.tool_profiles import TOOL_PROFILES

RULE_NAME: str = "redundancy"
RULE_WEIGHT: int = 20


def _format_tool(name: str) -> str:
    return name.replace("_", " ").title()


def _group_tools_by_category(
    all_tools: list[ToolUsage],
) -> dict[str, list[ToolUsage]]:
    """Group tools by their profile category."""
    groups: dict[str, list[ToolUsage]] = defaultdict(list)
    for t in all_tools:
        profile = TOOL_PROFILES.get(t.tool.lower())
        if profile is not None:
            groups[profile.category.value].append(t)
    return groups


def _tools_overlap(tool_a: str, tool_b: str) -> bool:
    """Return True if the two tools are listed as overlapping each other."""
    profile_a = TOOL_PROFILES.get(tool_a.lower())
    profile_b = TOOL_PROFILES.get(tool_b.lower())
    if profile_a is None or profile_b is None:
        return False
    return (
        tool_b.lower() in [t.lower() for t in profile_a.overlap_tools]
        or tool_a.lower() in [t.lower() for t in profile_b.overlap_tools]
    )


def evaluate(
    tool: ToolUsage,
    team_size: int,
    primary_use_case: UseCase,
    all_tools: list[ToolUsage],
) -> Recommendation | None:
    """Flag *tool* if it overlaps with other tools in the stack.

    We only emit a recommendation for the **more expensive** tool in each
    overlapping pair (to avoid duplicate recommendations for the same pair).
    """
    profile = TOOL_PROFILES.get(tool.tool.lower())
    if profile is None:
        return None

    category = profile.category.value
    groups = _group_tools_by_category(all_tools)
    siblings = groups.get(category, [])

    # Gather overlapping siblings (cheaper or equal — we recommend dropping
    # the MORE expensive one, so we fire on the expensive tool)
    overlapping = [
        s
        for s in siblings
        if s.tool.lower() != tool.tool.lower()
        and _tools_overlap(tool.tool, s.tool)
    ]

    if not overlapping:
        return None

    # Count total tools in this category (including this one)
    group_size = len(siblings)

    # Only fire for the most expensive tool in the overlap group to avoid
    # duplicate recommendations.  If there's a tie, fire for the one that
    # sorts later alphabetically (deterministic).
    all_in_group = [tool, *overlapping]
    most_expensive = max(
        all_in_group,
        key=lambda t: (t.monthly_spend, t.tool),
    )
    if most_expensive.tool.lower() != tool.tool.lower():
        return None  # another tool in the group will get flagged instead

    # ── Coding tools ────────────────────────────────────────────────────
    if category == "coding":
        cheapest = min(overlapping, key=lambda t: t.monthly_spend)
        if group_size >= 3:
            severity = Severity.HIGH
            confidence = Confidence.HIGH
            issue = (
                f"Your stack includes {group_size} coding AI tools "
                f"({', '.join(_format_tool(s.tool) for s in siblings)}). "
                f"Significant functional overlap exists."
            )
        else:
            severity = Severity.MEDIUM
            confidence = Confidence.MEDIUM
            issue = (
                f"Both {_format_tool(tool.tool)} and "
                f"{_format_tool(cheapest.tool)} are coding-focused AI tools "
                f"with overlapping capabilities."
            )

        monthly_savings = tool.monthly_spend  # drop the expensive one
        return Recommendation(
            tool=tool.tool,
            severity=severity,
            issue=issue,
            recommendation=(
                f"Consolidate to a single coding tool. "
                f"{_format_tool(cheapest.tool)} (${cheapest.monthly_spend:.0f}/mo) "
                f"covers similar functionality at a lower cost, or evaluate which "
                f"tool your team prefers and standardize."
            ),
            reasoning=(
                f"Running multiple coding AI assistants creates context-switching "
                f"overhead and duplicates spend. Most teams find a single tool "
                f"sufficient after an adjustment period."
            ),
            estimated_monthly_savings=round(monthly_savings, 2),
            estimated_annual_savings=round(monthly_savings * 12, 2),
            confidence=confidence,
        )

    # ── Productivity tools ──────────────────────────────────────────────
    if category == "productivity":
        if group_size >= 3:
            severity = Severity.HIGH
            confidence = Confidence.HIGH
        else:
            severity = Severity.MEDIUM
            confidence = Confidence.MEDIUM

        cheapest = min(overlapping, key=lambda t: t.monthly_spend)
        monthly_savings = tool.monthly_spend

        return Recommendation(
            tool=tool.tool,
            severity=severity,
            issue=(
                f"Your stack includes {group_size} general-purpose AI assistants "
                f"({', '.join(_format_tool(s.tool) for s in siblings)}). "
                f"These tools serve broadly similar use cases."
            ),
            recommendation=(
                f"Evaluate consolidating to one or two assistants. "
                f"{_format_tool(cheapest.tool)} (${cheapest.monthly_spend:.0f}/mo) "
                f"may be sufficient, or keep the one that best fits your "
                f"{primary_use_case.value} workflow."
            ),
            reasoning=(
                f"General-purpose AI assistants have significant functional "
                f"overlap for most workflows. Consolidation reduces per-seat "
                f"costs and simplifies vendor management."
            ),
            estimated_monthly_savings=round(monthly_savings, 2),
            estimated_annual_savings=round(monthly_savings * 12, 2),
            confidence=confidence,
        )

    # ── API tools ───────────────────────────────────────────────────────
    if category == "api":
        # API tools might be intentionally diverse (different model
        # strengths), so flag at LOW severity.
        cheapest = min(overlapping, key=lambda t: t.monthly_spend)
        monthly_savings = max(tool.monthly_spend * 0.3, 0.0)  # conservative

        return Recommendation(
            tool=tool.tool,
            severity=Severity.LOW,
            issue=(
                f"Multiple API providers detected "
                f"({', '.join(_format_tool(s.tool) for s in siblings)}). "
                f"Some usage may overlap."
            ),
            recommendation=(
                f"Audit API usage logs to identify whether both providers are "
                f"necessary. Consolidating to a single provider can simplify "
                f"billing and potentially unlock volume discounts."
            ),
            reasoning=(
                f"Some teams intentionally use multiple API providers for model "
                f"diversity, but many carry redundant integrations from earlier "
                f"experimentation. A usage audit can clarify."
            ),
            estimated_monthly_savings=round(monthly_savings, 2),
            estimated_annual_savings=round(monthly_savings * 12, 2),
            confidence=Confidence.LOW,
        )

    return None
