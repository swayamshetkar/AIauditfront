"""POST /api/save-lead — capture a lead after an audit."""

import logging

from fastapi import APIRouter, HTTPException, Request

from app.middleware.rate_limiter import LEAD_RATE_LIMIT, limiter
from app.schemas import AuditResult, LeadInput, LeadResponse
from app.services.email_service import send_audit_confirmation
from app.services.supabase import get_audit_by_public_id, store_lead

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["leads"])


@router.post("/save-lead", response_model=LeadResponse)
@limiter.limit(LEAD_RATE_LIMIT)
async def save_lead(request: Request, lead: LeadInput) -> LeadResponse:
    """Capture a lead, send a confirmation email, and return success.

    The ``website`` field is a honeypot — any non-empty value means the
    submission came from a bot and is silently rejected with a fake
    success response.
    """
    # Honeypot check — bots fill hidden fields
    if lead.website:
        logger.info("Honeypot triggered for %s — rejecting silently", lead.email)
        return LeadResponse(success=True, message="Thank you! We'll be in touch.")

    # Persist lead
    await store_lead(lead)

    # Send confirmation email if we have an associated audit
    if lead.audit_id:
        audit_row = await get_audit_by_public_id(lead.audit_id)
        if audit_row and "audit_json" in audit_row:
            audit_result = AuditResult.model_validate(audit_row["audit_json"])
            await send_audit_confirmation(lead.email, lead.audit_id, audit_result)

    return LeadResponse(success=True, message="Thank you! We'll be in touch.")
