"""Rate limiting middleware powered by slowapi."""

from __future__ import annotations

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

# ---------------------------------------------------------------------------
# Limiter instance — imported by main.py and route modules
# ---------------------------------------------------------------------------

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.rate_limit_per_minute}/minute"],
)

# Per-route limit strings (used as decorators on individual endpoints)
AUDIT_RATE_LIMIT: str = f"{settings.rate_limit_per_minute}/minute"
LEAD_RATE_LIMIT: str = "5/minute"
SUMMARY_RATE_LIMIT: str = "10/minute"
