"""Weighted scoring system for AI spend audits."""

from __future__ import annotations

from app.engine.rules import ALL_RULES
from app.schemas import Recommendation, ScoreBreakdown


def compute_score(
    recommendations: list[Recommendation], rule_scores: dict[str, float]
) -> tuple[int, str, list[ScoreBreakdown]]:
    """Compute the deterministic overspend score based on triggered rules.

    Score is from 0 to 100.
    """
    rule_weights = {
        rule.RULE_NAME: rule.RULE_WEIGHT
        for rule in ALL_RULES
        if hasattr(rule, "RULE_WEIGHT") and rule.RULE_WEIGHT > 0
    }
    total_possible_weight = sum(rule_weights.values())

    if total_possible_weight == 0:
        return 0, "Efficient", []

    breakdowns: list[ScoreBreakdown] = []
    total_score = 0.0

    for rule_name, weight in rule_weights.items():
        severity_factor = rule_scores.get(rule_name, 0.0)

        # Rule's contribution to the final 0-100 score
        weighted_score = (weight * severity_factor / total_possible_weight) * 100.0

        # Raw score out of 100 for this specific rule
        raw_score = severity_factor * 100.0

        total_score += weighted_score

        breakdowns.append(
            ScoreBreakdown(
                rule=rule_name,
                weight=weight,
                raw_score=round(raw_score, 1),
                weighted_score=round(weighted_score, 1),
            )
        )

    final_score = int(round(total_score))
    final_score = max(0, min(100, final_score))

    if final_score <= 20:
        label = "Efficient"
    elif final_score <= 50:
        label = "Moderate optimization possible"
    elif final_score <= 80:
        label = "Significant overspend"
    else:
        label = "Severe inefficiency"

    return final_score, label, breakdowns
