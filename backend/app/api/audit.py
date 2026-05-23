"""POST /api/audit — run an AI spend audit and persist it."""

import logging
from datetime import UTC, datetime

from fastapi import APIRouter, Request
from nanoid import generate as nanoid

from app.engine import run_audit
from app.middleware.rate_limiter import AUDIT_RATE_LIMIT, limiter
from app.schemas import AuditInput, AuditResponse
from app.services.supabase import store_audit

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["audit"])

# nanoid alphabet — URL-safe, no look-alikes
_NANOID_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_NANOID_SIZE = 12


@router.post("/audit", response_model=AuditResponse)
@limiter.limit(AUDIT_RATE_LIMIT)
async def create_audit(request: Request, payload: AuditInput) -> AuditResponse:
    """Run the deterministic audit engine, persist the result, and return it.

    Steps:
    1. Pydantic validates the input automatically.
    2. Execute the rule-based audit engine.
    3. Generate a unique, URL-safe ``public_id`` via nanoid.
    4. Store in Supabase (gracefully degrades if not configured).
    5. Return the ``AuditResponse``.
    """
    # Run engine
    audit_result = run_audit(payload)

    # Generate public ID
    public_id: str = nanoid(alphabet=_NANOID_ALPHABET, size=_NANOID_SIZE)

    # Persist (fire-and-forget — don't fail the request on DB errors)
    await store_audit(public_id, payload, audit_result)

    created_at = datetime.now(UTC).isoformat()

    return AuditResponse(
        public_id=public_id,
        audit=audit_result,
        created_at=created_at,
    )
