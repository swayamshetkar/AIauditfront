"""Seat efficiency rule — flags over- or under-provisioned seat licenses.

Weight: 15 / 100
"""

from __future__ import annotations

from app.schemas import Confidence, Recommendation, Severity, ToolUsage, UseCase
from app.tool_profiles import TOOL_PROFILES

RULE_NAME: str = "seat_efficiency"
RULE_WEIGHT: int = 15

# Thresholds
_EXCESS_THRESHOLD: float = 1.2  # seats > team_size × 1.2 → excess
_UNDER_THRESHOLD: float = 0.5   # seats < team_size × 0.5 → under-licensed


def _format_tool(name: str) -> str:
    return name.replace("_", " ").title()


def _has_seat_pricing(tool: ToolUsage) -> bool:
    """Return True if the tool uses seat-based pricing."""
    profile = TOOL_PROFILES.get(tool.tool.lower())
    if profile is not None:
        return profile.pricing_type.value in ("seat", "seat+api")
    return False


def evaluate(
    tool: ToolUsage,
    team_size: int,
    primary_use_case: UseCase,
    all_tools: list[ToolUsage],
) -> Recommendation | None:
    """Flag seat count mismatches."""
    if not _has_seat_pricing(tool):
        return None

    tool_label = _format_tool(tool.tool)

    # ── Unknown seat count — advisory note ──────────────────────────────
    if tool.seats is None:
        return Recommendation(
            tool=tool.tool,
            severity=Severity.LOW,
            issue=(
                f"Seat count for {tool_label} is not specified. Cannot verify "
                f"license utilization."
            ),
            recommendation=(
                f"Review your {tool_label} admin dashboard to verify active "
                f"seat count. Unused licenses represent direct cost waste."
            ),
            reasoning=(
                f"{tool_label} uses seat-based pricing. Without knowing the "
                f"exact seat count, it's not possible to determine whether "
                f"you're paying for unused licenses."
            ),
            estimated_monthly_savings=0.0,
            estimated_annual_savings=0.0,
            confidence=Confidence.LOW,
        )

    seats = tool.seats

    # ── Excess seats ────────────────────────────────────────────────────
    if seats > team_size * _EXCESS_THRESHOLD:
        excess = seats - team_size
        per_seat_price = tool.monthly_spend / max(seats, 1)
        monthly_savings = excess * per_seat_price

        # Determine severity by how many excess seats
        excess_ratio = seats / max(team_size, 1)
        if excess_ratio >= 2.0:
            severity = Severity.HIGH
            confidence = Confidence.HIGH
        elif excess_ratio >= 1.5:
            severity = Severity.MEDIUM
            confidence = Confidence.HIGH
        else:
            severity = Severity.LOW
            confidence = Confidence.MEDIUM

        return Recommendation(
            tool=tool.tool,
            severity=severity,
            issue=(
                f"{tool_label} has {seats} seats provisioned for a team of "
                f"{team_size} — {excess} seat{'s' if excess > 1 else ''} "
                f"appear unused."
            ),
            recommendation=(
                f"Reduce {tool_label} seat count from {seats} to {team_size}. "
                f"At ${per_seat_price:.2f}/seat/mo, this saves "
                f"${monthly_savings:.2f}/mo."
            ),
            reasoning=(
                "Each unused seat is a direct cost with zero productivity "
                "return. Seat counts should be reviewed quarterly and aligned "
                "to actual headcount. Consider enabling just-in-time "
                "provisioning if available."
            ),
            estimated_monthly_savings=round(monthly_savings, 2),
            estimated_annual_savings=round(monthly_savings * 12, 2),
            confidence=confidence,
        )

    # ── Under-licensed (informational, not savings) ─────────────────────
    if seats < team_size * _UNDER_THRESHOLD:
        return Recommendation(
            tool=tool.tool,
            severity=Severity.LOW,
            issue=(
                f"{tool_label} has only {seats} seat{'s' if seats > 1 else ''} "
                f"for a team of {team_size}. Some team members may lack access."
            ),
            recommendation=(
                f"Verify that all team members who need {tool_label} access "
                f"have it. Under-licensing can reduce team productivity."
            ),
            reasoning=(
                "While fewer seats reduce cost, under-licensing can create "
                "bottlenecks where team members wait for access or resort to "
                "less effective alternatives."
            ),
            estimated_monthly_savings=0.0,
            estimated_annual_savings=0.0,
            confidence=Confidence.LOW,
        )

    return None
