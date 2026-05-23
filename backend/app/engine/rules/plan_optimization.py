"""Plan optimization rule — recommends cheaper plans from the same vendor.

Weight: 0 (generates savings recommendations but does not contribute to the
overspend score, since plan-level optimization is an opportunity rather than
a clear mistake).
"""

from __future__ import annotations

from app.schemas import Confidence, Recommendation, Severity, ToolUsage, UseCase
from app.tool_profiles import TOOL_PROFILES
from app.pricing.registry import get_all_plans, get_plan_price, PRICING_REGISTRY

RULE_NAME: str = "plan_optimization"
RULE_WEIGHT: int = 0


def _format_tool(name: str) -> str:
    return name.replace("_", " ").title()


def _format_plan(name: str) -> str:
    return name.replace("_", " ").title()


def evaluate(
    tool: ToolUsage,
    team_size: int,
    primary_use_case: UseCase,
    all_tools: list[ToolUsage],
) -> Recommendation | None:
    """Suggest cheaper plans when usage patterns indicate a downgrade is safe."""
    current_plan = tool.plan.lower()
    current_price = get_plan_price(tool.tool, current_plan)
    seats = tool.seats if tool.seats is not None else team_size

    # If we don't know the current price, we can't compare
    if current_price is None:
        return None

    profile = TOOL_PROFILES.get(tool.tool.lower())
    use_case_str = primary_use_case.value

    # ── Team/business plan for small team → individual plans ────────────
    # (enterprise_overkill covers team_size <= 2 already, so focus on 3-4)
    if current_plan in ("business", "teams", "team_standard", "team_premium"):
        if team_size < 5:
            all_plans = get_all_plans(tool.tool)
            individual_plans = [
                p
                for p in all_plans
                if p not in (
                    "enterprise",
                    "business",
                    "teams",
                    "team_standard",
                    "team_premium",
                    "free",
                )
            ]
            cheaper: list[tuple[float, str]] = []
            for p in individual_plans:
                price = get_plan_price(tool.tool, p)
                if price is not None and price < current_price:
                    cheaper.append((price, p))
            if cheaper:
                cheaper.sort()
                best_price, best_plan = cheaper[0]
                savings_per_seat = current_price - best_price
                monthly_savings = savings_per_seat * seats
                return Recommendation(
                    tool=tool.tool,
                    severity=Severity.LOW,
                    issue=(
                        f"{_format_tool(tool.tool)} is on the "
                        f"{_format_plan(current_plan)} plan "
                        f"(${current_price:.0f}/seat/mo) with a team of "
                        f"{team_size}."
                    ),
                    recommendation=(
                        f"Consider {seats} individual "
                        f"{_format_plan(best_plan)} licenses at "
                        f"${best_price:.0f}/seat/mo instead of a team plan."
                    ),
                    reasoning=(
                        f"At your team size, individual licenses can be more "
                        f"cost-effective while providing equivalent AI "
                        f"capabilities. Team management features may not "
                        f"justify the premium."
                    ),
                    estimated_monthly_savings=round(monthly_savings, 2),
                    estimated_annual_savings=round(monthly_savings * 12, 2),
                    confidence=Confidence.MEDIUM,
                )

    # ── Power-user tier when usage doesn't demand it ────────────────────
    power_plans = {"pro_plus", "ultra", "max_5x", "max_20x", "max"}
    if current_plan in power_plans:
        # Heuristic: if the use case isn't the tool's primary strength,
        # the user likely doesn't need the highest tier.
        tool_ideal = (
            profile.ideal_use_cases if profile else []
        )
        not_primary_strength = use_case_str not in tool_ideal

        all_plans = get_all_plans(tool.tool)
        cheaper_plans: list[tuple[float, str]] = []
        for p in all_plans:
            if p in power_plans or p in ("enterprise", "free"):
                continue
            price = get_plan_price(tool.tool, p)
            if price is not None and 0 < price < current_price:
                cheaper_plans.append((price, p))

        if cheaper_plans and not_primary_strength:
            cheaper_plans.sort()
            best_price, best_plan = cheaper_plans[0]
            savings_per_seat = current_price - best_price
            monthly_savings = savings_per_seat * seats
            return Recommendation(
                tool=tool.tool,
                severity=Severity.MEDIUM,
                issue=(
                    f"{_format_tool(tool.tool)} is on the "
                    f"{_format_plan(current_plan)} tier "
                    f"(${current_price:.0f}/seat/mo), but your primary "
                    f"workflow ({use_case_str}) may not require this level."
                ),
                recommendation=(
                    f"Downgrade to the {_format_plan(best_plan)} plan "
                    f"(${best_price:.0f}/seat/mo). The additional capacity "
                    f"of the {_format_plan(current_plan)} tier is most "
                    f"valuable for heavy {', '.join(tool_ideal)} usage."
                ),
                reasoning=(
                    f"Power-user tiers provide higher usage limits and premium "
                    f"model access. For {use_case_str} workflows that don't "
                    f"heavily leverage {_format_tool(tool.tool)}'s advanced "
                    f"features, a standard plan is typically sufficient."
                ),
                estimated_monthly_savings=round(monthly_savings, 2),
                estimated_annual_savings=round(monthly_savings * 12, 2),
                confidence=Confidence.MEDIUM,
            )

    # ── Free tier suggestion for solo users with low-fit tools ──────────
    if team_size == 1 and profile is not None:
        if use_case_str not in profile.ideal_use_cases:
            free_price = get_plan_price(tool.tool, "free")
            if free_price is not None and free_price == 0.0 and current_price > 0:
                monthly_savings = current_price * seats
                return Recommendation(
                    tool=tool.tool,
                    severity=Severity.LOW,
                    issue=(
                        f"{_format_tool(tool.tool)} ({_format_plan(current_plan)} "
                        f"at ${current_price:.0f}/mo) may not be essential for "
                        f"your {use_case_str} workflow."
                    ),
                    recommendation=(
                        f"Consider downgrading to the free tier. For "
                        f"{use_case_str} workflows, the free tier's limits "
                        f"may be sufficient, especially if this isn't your "
                        f"primary tool."
                    ),
                    reasoning=(
                        f"Solo users whose primary workflow doesn't align "
                        f"with {_format_tool(tool.tool)}'s strengths often "
                        f"find that the free tier covers their occasional "
                        f"usage adequately."
                    ),
                    estimated_monthly_savings=round(monthly_savings, 2),
                    estimated_annual_savings=round(monthly_savings * 12, 2),
                    confidence=Confidence.LOW,
                )

    return None
