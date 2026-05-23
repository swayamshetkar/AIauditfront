"""Main orchestrator for the deterministic audit engine."""

from __future__ import annotations

from app.engine.rules import ALL_RULES
from app.engine.scoring import compute_score
from app.schemas import AuditInput, AuditResult, Recommendation, Severity


def run_audit(input_data: AuditInput) -> AuditResult:
    """Run all audit rules against the input data and compute final result."""
    recommendations: list[Recommendation] = []
    rule_scores: dict[str, float] = {}

    severity_to_factor = {
        Severity.LOW: 0.3,
        Severity.MEDIUM: 0.6,
        Severity.HIGH: 1.0,
    }

    # Evaluate each tool against all rules
    for tool in input_data.tools:
        for rule in ALL_RULES:
            # Plan optimization doesn't evaluate individual tools in the same way, but let's assume all rules follow the interface
            result = rule.evaluate(tool, input_data.team_size, input_data.primary_use_case, input_data.tools)
            if result:
                recommendations.append(result)

                # Track highest severity for scoring
                severity_factor = severity_to_factor.get(result.severity, 0.0)
                current_max = rule_scores.get(rule.RULE_NAME, 0.0)
                rule_scores[rule.RULE_NAME] = max(current_max, severity_factor)

    # Compute total score
    score, label, breakdown = compute_score(recommendations, rule_scores)

    # Aggregate savings and spend
    # Note: Using set to avoid double-counting savings for the same tool/issue might be needed in a real scenario,
    # but based on the prompt, simple sum is acceptable for MVP.
    total_monthly_savings = sum(r.estimated_monthly_savings for r in recommendations)
    total_annual_savings = sum(r.estimated_annual_savings for r in recommendations)
    total_spend = sum(t.monthly_spend for t in input_data.tools)

    # Cap total savings at total spend
    total_monthly_savings = min(total_monthly_savings, total_spend)
    total_annual_savings = min(total_annual_savings, total_spend * 12)

    tools_analyzed = list({t.tool for t in input_data.tools})

    return AuditResult(
        overspend_score=score,
        score_label=label,
        score_breakdown=breakdown,
        recommendations=recommendations,
        total_monthly_spend=round(total_spend, 2),
        total_estimated_monthly_savings=round(total_monthly_savings, 2),
        total_estimated_annual_savings=round(total_annual_savings, 2),
        tool_count=len(input_data.tools),
        team_size=input_data.team_size,
        primary_use_case=input_data.primary_use_case,
        tools_analyzed=tools_analyzed,
    )
