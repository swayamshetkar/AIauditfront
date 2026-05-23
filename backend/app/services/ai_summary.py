"""AI-powered audit summary generation with Anthropic → OpenAI → fallback chain."""

from __future__ import annotations

import asyncio
import logging

import openai

from app.config import settings
from app.schemas import AuditResult

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------

SUMMARY_PROMPT = """\
You are a financial optimization consultant specializing in AI tool spend \
for startups and engineering teams.

Generate a concise ~100-word personalized summary paragraph for this AI spend audit.

Audit Details:
- Team size: {team_size}
- Primary use case: {primary_use_case}
- Tools analyzed: {tools}
- Total monthly spend: ${total_monthly_spend:.2f}
- Total potential monthly savings: ${total_monthly_savings:.2f}
- Total potential annual savings: ${total_annual_savings:.2f}
- Overspend score: {overspend_score}/100 ({score_label})
- Key issues: {issues}

Guidelines:
- Be direct and professional, like a CFO advisor
- Lead with the most impactful finding
- Mention specific dollar amounts
- If savings are minimal (<$100/mo), acknowledge the team is spending well
- Do NOT use marketing language or hyperbole
- Do NOT mention Credex or any specific vendor
- End with a forward-looking recommendation
"""

# ---------------------------------------------------------------------------
# AI timeout (seconds)
# ---------------------------------------------------------------------------

_AI_TIMEOUT = 10


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_prompt(audit_result: AuditResult) -> str:
    """Fill in the prompt template with audit data."""
    issues = "; ".join(
        f"{r.tool}: {r.issue}" for r in audit_result.recommendations[:5]
    ) or "No major issues found"

    return SUMMARY_PROMPT.format(
        team_size=audit_result.team_size,
        primary_use_case=audit_result.primary_use_case.value,
        tools=", ".join(audit_result.tools_analyzed),
        total_monthly_spend=audit_result.total_monthly_spend,
        total_monthly_savings=audit_result.total_estimated_monthly_savings,
        total_annual_savings=audit_result.total_estimated_annual_savings,
        overspend_score=audit_result.overspend_score,
        score_label=audit_result.score_label,
        issues=issues,
    )


async def _try_openrouter(prompt: str) -> str | None:
    """Attempt summary generation via OpenRouter."""
    if not settings.openrouter_api_key:
        return None

    try:
        client = openai.AsyncOpenAI(
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model="deepseek/deepseek-chat",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
                extra_headers={
                    "HTTP-Referer": settings.app_url,
                    "X-Title": "AIRev Audit"
                }
            ),
            timeout=_AI_TIMEOUT,
        )
        text = (response.choices[0].message.content or "").strip()
        return text if text else None
    except TimeoutError:
        logger.warning("OpenRouter request timed out after %ds", _AI_TIMEOUT)
        return None
    except Exception:
        logger.exception("OpenRouter summary generation failed")
        return None


def _build_fallback_summary(audit_result: AuditResult) -> str:
    """Template-based summary that requires no API call.

    Still personalised using the audit data so it reads well.
    """
    savings = audit_result.total_estimated_monthly_savings
    annual = audit_result.total_estimated_annual_savings
    score = audit_result.overspend_score
    tools = ", ".join(audit_result.tools_analyzed)

    if savings < 100:
        return (
            f"Your team of {audit_result.team_size} is managing AI spend well across "
            f"{tools}. At ${audit_result.total_monthly_spend:,.2f}/month, your "
            f"overspend score of {score}/100 ({audit_result.score_label}) suggests "
            f"minimal waste. Potential savings are modest at ${savings:,.2f}/month. "
            f"Continue monitoring usage as your team scales to maintain this efficiency."
        )

    top = audit_result.recommendations[0] if audit_result.recommendations else None
    top_line = (
        f"The biggest opportunity is in {top.tool} — {top.issue.lower()}."
        if top
        else ""
    )

    return (
        f"Across {len(audit_result.tools_analyzed)} tools, your team of "
        f"{audit_result.team_size} spends ${audit_result.total_monthly_spend:,.2f}/month "
        f"with an overspend score of {score}/100 ({audit_result.score_label}). "
        f"{top_line} "
        f"Implementing the recommended changes could save ${savings:,.2f}/month "
        f"(${annual:,.2f}/year). Prioritise the highest-severity items first."
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


async def generate_summary(audit_result: AuditResult) -> tuple[str, str]:
    """Generate a personalised audit summary.

    Tries OpenRouter first, then a deterministic fallback.

    Returns:
        A ``(summary_text, source)`` tuple where *source* is ``"ai"`` or
        ``"fallback"``.
    """
    prompt = _build_prompt(audit_result)

    # 1. Try OpenRouter
    text = await _try_openrouter(prompt)
    if text:
        logger.info("Summary generated via OpenRouter")
        return text, "ai"

    # 2. Deterministic fallback
    logger.info("Using fallback summary (no AI provider available)")
    return _build_fallback_summary(audit_result), "fallback"
