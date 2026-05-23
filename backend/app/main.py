"""FastAPI application entry point — mounts all routers and middleware."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api import audit, gated_audit, lead, public_audit, summary, tools
from app.middleware.rate_limiter import limiter

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)

# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AIRev — AI Spend Audit API",
    description="Deterministic, rule-based AI tool spend audit engine",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

# CORS — permissive in dev, tighten via env vars for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://a-iauditfront.vercel.app",
        "https://a-iauditfront-swayamshetkars-projects.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(audit.router)
app.include_router(gated_audit.router)
app.include_router(lead.router)
app.include_router(summary.router)
app.include_router(public_audit.router)
app.include_router(tools.router)

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get("/health", tags=["infra"])
async def health_check() -> dict[str, str]:
    """Simple liveness probe."""
    return {"status": "ok"}
