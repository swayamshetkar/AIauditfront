"""POST /api/generate-summary — AI-powered audit summary generation."""

import logging

from fastapi import APIRouter, Request

from app.middleware.rate_limiter import SUMMARY_RATE_LIMIT, limiter
from app.schemas import SummaryRequest, SummaryResponse
from app.services.ai_summary import generate_summary

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["summary"])


@router.post("/generate-summary", response_model=SummaryResponse)
@limiter.limit(SUMMARY_RATE_LIMIT)
async def create_summary(request: Request, body: SummaryRequest) -> SummaryResponse:
    """Generate a personalised executive summary for an audit result.

    Uses the OpenRouter → fallback chain defined in
    ``app.services.ai_summary``.
    """
    summary_text, source = await generate_summary(body.audit_result)

    return SummaryResponse(summary=summary_text, source=source)
