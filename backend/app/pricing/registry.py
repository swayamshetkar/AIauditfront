"""Unified pricing registry — single entry point for all tool pricing data.

Aggregates per-tool pricing modules into a single flat registry and exposes
convenience helpers used by the audit engine.
"""

from __future__ import annotations

from app.pricing.anthropic_api import PRICING as ANTHROPIC_API_PRICING
from app.pricing.chatgpt import PRICING as CHATGPT_PRICING
from app.pricing.claude import PRICING as CLAUDE_PRICING
from app.pricing.copilot import PRICING as COPILOT_PRICING
from app.pricing.cursor import PRICING as CURSOR_PRICING
from app.pricing.gemini import PRICING as GEMINI_PRICING
from app.pricing.gemini_api import PRICING as GEMINI_API_PRICING
from app.pricing.openai_api import PRICING as OPENAI_API_PRICING
from app.pricing.windsurf import PRICING as WINDSURF_PRICING

# ---------------------------------------------------------------------------
# Unified registry: tool_name → {plan_name → plan_data}
# ---------------------------------------------------------------------------

PRICING_REGISTRY: dict[str, dict[str, dict]] = {
    "cursor": CURSOR_PRICING,
    "github_copilot": COPILOT_PRICING,
    "windsurf": WINDSURF_PRICING,
    "chatgpt": CHATGPT_PRICING,
    "claude": CLAUDE_PRICING,
    "gemini": GEMINI_PRICING,
    "openai_api": OPENAI_API_PRICING,
    "anthropic_api": ANTHROPIC_API_PRICING,
    "gemini_api": GEMINI_API_PRICING,
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def get_plan_price(tool: str, plan: str) -> float | None:
    """Get monthly price for a tool+plan.

    Returns ``None`` for custom / usage-based plans where no fixed
    monthly price exists.
    """
    tool_plans = PRICING_REGISTRY.get(tool.lower())
    if tool_plans is None:
        return None
    plan_data = tool_plans.get(plan.lower())
    if plan_data is None:
        return None
    return plan_data.get("monthly")


def get_optimal_plan(tool: str, seats: int) -> str | None:
    """Return the most cost-effective plan for *seats* users.

    Finds the cheapest non-free plan whose ``min_seats`` requirement (if
    any) is satisfied by *seats* and whose ``max_seats`` ceiling (if any)
    is not exceeded.  Plans with ``monthly=None`` (custom / usage-based)
    are excluded from the comparison.

    Returns ``None`` when no qualifying plan exists.
    """
    tool_plans = PRICING_REGISTRY.get(tool.lower())
    if tool_plans is None:
        return None

    effective_seats = max(seats, 1)
    candidates: list[tuple[float, str]] = []

    for plan_name, plan_data in tool_plans.items():
        price = plan_data.get("monthly")
        if price is None or price <= 0:
            continue  # skip free and custom/usage-based

        min_seats = plan_data.get("min_seats")
        max_seats = plan_data.get("max_seats")

        if min_seats is not None and effective_seats < min_seats:
            continue
        if max_seats is not None and effective_seats > max_seats:
            continue

        candidates.append((price, plan_name))

    if not candidates:
        return None
    candidates.sort()
    return candidates[0][1]


def get_all_plans(tool: str) -> list[str]:
    """Return all available plan names for *tool*.

    Returns an empty list when *tool* is not found in the registry.
    """
    tool_plans = PRICING_REGISTRY.get(tool.lower())
    if tool_plans is None:
        return []
    return list(tool_plans.keys())
