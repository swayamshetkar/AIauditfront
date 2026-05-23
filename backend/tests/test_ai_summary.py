"""Tests for the AI summary generation layer."""

from unittest.mock import AsyncMock, patch

import pytest

from app.schemas import AuditResult, Confidence, Recommendation, ScoreBreakdown, Severity, UseCase
from app.services.ai_summary import generate_summary


@pytest.fixture
def mock_audit_result() -> AuditResult:
    return AuditResult(
        overspend_score=39,
        score_label="Moderate optimization possible",
        score_breakdown=[
            ScoreBreakdown(
                rule="enterprise_overkill", weight=40, raw_score=100.0, weighted_score=29.6
            )
        ],
        recommendations=[
            Recommendation(
                tool="github_copilot",
                severity=Severity.HIGH,
                issue="Github Copilot Enterprise plan is overkill.",
                recommendation="Downgrade to Pro.",
                reasoning="Small team does not need enterprise.",
                estimated_monthly_savings=100.0,
                estimated_annual_savings=1200.0,
                confidence=Confidence.HIGH,
            )
        ],
        total_monthly_spend=150.0,
        total_estimated_monthly_savings=100.0,
        total_estimated_annual_savings=1200.0,
        tool_count=1,
        team_size=5,
        primary_use_case=UseCase.CODING,
        tools_analyzed=["github_copilot"]
    )

@pytest.mark.asyncio
async def test_fallback_summary_generation(mock_audit_result: AuditResult) -> None:
    """If no API key is provided, it should cleanly use the fallback."""
    with patch("app.services.ai_summary.settings") as mock_settings:
        mock_settings.openrouter_api_key = ""
        text, source = await generate_summary(mock_audit_result)

        assert source == "fallback"
        assert "The biggest opportunity is in github_copilot" in text
        assert "100.00/month" in text

@pytest.mark.asyncio
@patch("app.services.ai_summary.openai.AsyncOpenAI")
async def test_successful_openrouter_summary(
    mock_openai_class, mock_audit_result: AuditResult
) -> None:
    """Valid key should return AI summary."""
    with patch("app.services.ai_summary.settings") as mock_settings:
        mock_settings.openrouter_api_key = "test-key"

        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock(message=AsyncMock(content="AI generated summary."))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        text, source = await generate_summary(mock_audit_result)

        assert source == "ai"
        assert text == "AI generated summary."

@pytest.mark.asyncio
@patch("app.services.ai_summary.openai.AsyncOpenAI")
async def test_openrouter_timeout_falls_back(
    mock_openai_class, mock_audit_result: AuditResult
) -> None:
    """If OpenRouter throws an exception, it should fallback without crashing."""
    with patch("app.services.ai_summary.settings") as mock_settings:
        mock_settings.openrouter_api_key = "test-key"

        mock_client = AsyncMock()
        mock_client.chat.completions.create.side_effect = Exception("API down")
        mock_openai_class.return_value = mock_client

        text, source = await generate_summary(mock_audit_result)

        assert source == "fallback"
