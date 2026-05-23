"""POST /api/audit-preview and /api/audit-and-send for gated flow."""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Request
from nanoid import generate as nanoid

from app.engine import run_audit
from app.middleware.rate_limiter import AUDIT_RATE_LIMIT, limiter
from app.schemas import AuditInput, AuditPreviewResponse, GatedAuditInput, LeadInput, LeadResponse
from app.services.supabase import store_audit, store_lead
from app.services.email_service import send_audit_confirmation

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["gated_audit"])

_NANOID_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_NANOID_SIZE = 12


@router.post("/audit-preview", response_model=AuditPreviewResponse)
@limiter.limit(AUDIT_RATE_LIMIT)
async def preview_audit(request: Request, payload: AuditInput) -> AuditPreviewResponse:
    """Run the audit engine and return ONLY high-level metrics.
    
    This does not save to the database, does not generate a public_id, and
    does not expose the detailed breakdown to the client.
    """
    audit_result = run_audit(payload)
    
    return AuditPreviewResponse(
        overspend_score=audit_result.overspend_score,
        score_label=audit_result.score_label,
        total_monthly_spend=audit_result.total_monthly_spend,
        total_estimated_monthly_savings=audit_result.total_estimated_monthly_savings,
        total_estimated_annual_savings=audit_result.total_estimated_annual_savings,
    )


@router.post("/audit-and-send", response_model=LeadResponse)
@limiter.limit(AUDIT_RATE_LIMIT)
async def audit_and_send(request: Request, payload: GatedAuditInput) -> LeadResponse:
    """Run the audit, save to DB, capture lead, and send email.
    
    This ensures the `public_id` and full audit report are NEVER returned
    to the frontend. The only way the user gets it is via the email.
    """
    # 1. Run engine
    audit_result = run_audit(payload)

    # 2. Generate public ID & Persist Audit
    public_id: str = nanoid(alphabet=_NANOID_ALPHABET, size=_NANOID_SIZE)
    await store_audit(public_id, payload, audit_result)

    # 3. Persist Lead
    lead = LeadInput(
        email=payload.email,
        company_name=payload.company_name,
        role=payload.role,
        team_size=payload.team_size,
        audit_id=public_id,
        website=payload.website,
    )
    await store_lead(lead)

    # 4. Send Email
    await send_audit_confirmation(payload.email, public_id, audit_result)

    return LeadResponse(success=True, message="Audit saved and email sent successfully.")
