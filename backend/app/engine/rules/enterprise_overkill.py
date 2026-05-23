"""Enterprise overkill rule — flags expensive plans that exceed team needs.

Weight: 40 / 100  (heaviest rule — enterprise bloat is the #1 waste driver)
"""

from __future__ import annotations

from app.schemas import Confidence, Recommendation, Severity, ToolUsage, UseCase
from app.tool_profiles import TOOL_PROFILES
from app.pricing.registry import get_optimal_plan, get_plan_price

RULE_NAME: str = "enterprise_overkill"
RULE_WEIGHT: int = 40

# Plan names that indicate enterprise / team tiers
_ENTERPRISE_PLANS: frozenset[str] = frozenset({"enterprise"})
_TEAM_PLANS: frozenset[str] = frozenset({
    "business",
    "teams",
    "team_standard",
    "team_premium",
})
_POWER_USER_PLANS: frozenset[str] = frozenset({
    "pro_plus",
    "ultra",
    "max_5x",
    "max_20x",
    "max",
    "pro",  # ChatGPT Pro at $200/mo is a power-user plan
})

# ChatGPT "pro" is $200/mo — treat it as a power-user plan, not a normal pro.
_CHATGPT_PRO_PRICE_THRESHOLD: float = 100.0


def _format_tool(name: str) -> str:
    return name.replace("_", " ").title()


def _seats_or_team(tool: ToolUsage, team_size: int) -> int:
    """Best-effort seat count for savings math."""
    return tool.seats if tool.seats is not None else team_size


def evaluate(
    tool: ToolUsage,
    team_size: int,
    primary_use_case: UseCase,
    all_tools: list[ToolUsage],
) -> Recommendation | None:
    """Flag plans that are more expensive than the team needs."""
    profile = TOOL_PROFILES.get(tool.tool.lower())
    plan = tool.plan.lower()
    tool_label = _format_tool(tool.tool)
    seats = _seats_or_team(tool, team_size)

    # ── Enterprise plan on a small team ─────────────────────────────────
    if plan in _ENTERPRISE_PLANS:
        threshold = profile.enterprise_threshold if profile else 50
        if team_size < threshold:
            recommended_plan = get_optimal_plan(tool.tool, seats)
            recommended_price = (
                get_plan_price(tool.tool, recommended_plan)
                if recommended_plan
                else None
            )
            if recommended_price is not None and recommended_plan:
                savings_per_seat = max(
                    (tool.monthly_spend / max(seats, 1)) - recommended_price, 0.0
                )
                monthly_savings = savings_per_seat * seats
            else:
                monthly_savings = 0.0
                recommended_plan = "a standard"

            return Recommendation(
                tool=tool.tool,
                severity=Severity.HIGH,
                issue=(
                    f"{tool_label} Enterprise plan is designed for organizations "
                    f"with {threshold}+ seats. Your team of {team_size} is "
                    f"significantly below that threshold."
                ),
                recommendation=(
                    f"Downgrade to the {_format_tool(recommended_plan)} plan. "
                    f"Enterprise features like SSO, SCIM, and audit logs are "
                    f"unlikely to provide value at your current team size."
                ),
                reasoning=(
                    f"Enterprise plans carry a premium for compliance, security, "
                    f"and administrative features that teams under {threshold} "
                    f"members rarely require. The {_format_tool(recommended_plan)} "
                    f"plan includes all core functionality."
                ),
                estimated_monthly_savings=round(monthly_savings, 2),
                estimated_annual_savings=round(monthly_savings * 12, 2),
                confidence=Confidence.HIGH,
            )

    # ── Team/business plan for very small teams ─────────────────────────
    if plan in _TEAM_PLANS:
        if team_size <= 2:
            recommended_plan = get_optimal_plan(tool.tool, 1)
            recommended_price = (
                get_plan_price(tool.tool, recommended_plan)
                if recommended_plan
                else None
            )
            if recommended_price is not None and recommended_plan:
                savings_per_seat = max(
                    (tool.monthly_spend / max(seats, 1)) - recommended_price, 0.0
                )
                monthly_savings = savings_per_seat * seats
            else:
                monthly_savings = 0.0
                recommended_plan = "individual"

            return Recommendation(
                tool=tool.tool,
                severity=Severity.HIGH,
                issue=(
                    f"{tool_label} is on a team/business plan, but your team has "
                    f"only {team_size} member{'s' if team_size > 1 else ''}."
                ),
                recommendation=(
                    f"Switch to the {_format_tool(recommended_plan or 'individual')} "
                    f"plan. Team plans are designed for groups that need centralized "
                    f"billing and admin controls."
                ),
                reasoning=(
                    f"Team and business plans include administrative overhead costs "
                    f"(SSO, workspace management) that provide minimal benefit for "
                    f"individuals or pairs. An individual plan covers the same core "
                    f"AI capabilities."
                ),
                estimated_monthly_savings=round(monthly_savings, 2),
                estimated_annual_savings=round(monthly_savings * 12, 2),
                confidence=Confidence.HIGH,
            )

        if team_size <= 5:
            recommended_plan = get_optimal_plan(tool.tool, seats)
            recommended_price = (
                get_plan_price(tool.tool, recommended_plan)
                if recommended_plan
                else None
            )
            current_per_seat = tool.monthly_spend / max(seats, 1)
            if (
                recommended_price is not None
                and recommended_plan
                and recommended_price < current_per_seat
            ):
                savings_per_seat = current_per_seat - recommended_price
                monthly_savings = savings_per_seat * seats
                return Recommendation(
                    tool=tool.tool,
                    severity=Severity.MEDIUM,
                    issue=(
                        f"{tool_label} is on a team plan for a small team of "
                        f"{team_size}."
                    ),
                    recommendation=(
                        f"Evaluate the {_format_tool(recommended_plan)} plan at "
                        f"${recommended_price:.0f}/seat/mo. At your team size, "
                        f"individual plans may be more cost-effective than team "
                        f"billing."
                    ),
                    reasoning=(
                        f"Team plans offer value through centralized management "
                        f"at scale. For teams of {team_size}, the per-seat premium "
                        f"may outweigh the administrative convenience."
                    ),
                    estimated_monthly_savings=round(monthly_savings, 2),
                    estimated_annual_savings=round(monthly_savings * 12, 2),
                    confidence=Confidence.MEDIUM,
                )

    # ── Power-user plans on small teams ─────────────────────────────────
    if plan in _POWER_USER_PLANS and team_size < 3:
        # Special handling: ChatGPT "pro" at $200/mo is genuinely power-user
        current_price = get_plan_price(tool.tool, plan)
        if current_price is not None and current_price >= _CHATGPT_PRO_PRICE_THRESHOLD:
            recommended_plan = get_optimal_plan(tool.tool, seats)
            recommended_price = (
                get_plan_price(tool.tool, recommended_plan)
                if recommended_plan
                else None
            )
            if recommended_price is not None and recommended_plan:
                savings_per_seat = max(current_price - recommended_price, 0.0)
                monthly_savings = savings_per_seat * seats
            else:
                monthly_savings = 0.0
                recommended_plan = "standard"

            return Recommendation(
                tool=tool.tool,
                severity=Severity.MEDIUM,
                issue=(
                    f"{tool_label} is on the {plan.replace('_', ' ')} tier "
                    f"(${current_price:.0f}/mo per seat) for a team of {team_size}."
                ),
                recommendation=(
                    f"Evaluate whether the additional capacity of the "
                    f"{plan.replace('_', ' ')} tier is fully utilized. The "
                    f"{_format_tool(recommended_plan)} plan may be sufficient."
                ),
                reasoning=(
                    f"Power-user plans provide significantly higher usage limits, "
                    f"but many users find that standard pro tiers cover their actual "
                    f"daily usage. Consider monitoring utilization before renewing."
                ),
                estimated_monthly_savings=round(monthly_savings, 2),
                estimated_annual_savings=round(monthly_savings * 12, 2),
                confidence=Confidence.MEDIUM,
            )

    return None
