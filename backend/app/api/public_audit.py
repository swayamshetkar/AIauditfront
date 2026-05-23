"""GET /api/audit/{public_id} — shareable, public audit result."""

import logging

from fastapi import APIRouter, HTTPException

from app.schemas import AuditResult
from app.services.supabase import get_audit_by_public_id

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["public"])


@router.get("/audit/{public_id}")
async def get_public_audit(public_id: str) -> dict:
    """Return a public audit result for sharing via URL.

    The response intentionally strips identifying details (no email, no
    company name) and includes hints for OG metadata generation on the
    frontend.
    """
    row = await get_audit_by_public_id(public_id)

    if row is None:
        raise HTTPException(status_code=404, detail="Audit not found")

    audit_json = row.get("audit_json")
    if audit_json is None:
        raise HTTPException(status_code=404, detail="Audit data unavailable")

    # Parse and re-serialise to guarantee schema compliance
    audit = AuditResult.model_validate(audit_json)

    return {
        "public_id": public_id,
        "audit": audit.model_dump(mode="json"),
        "created_at": row.get("created_at", ""),
        # OG metadata hints for the frontend
        "og": {
            "title": f"AI Spend Audit — Score: {audit.overspend_score}/100",
            "description": (
                f"A team of {audit.team_size} analyzed {audit.tool_count} AI tools. "
                f"Potential savings: ${audit.total_estimated_monthly_savings:,.2f}/mo."
            ),
        },
    }
