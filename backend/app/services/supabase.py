"""Supabase client and CRUD operations for audits and leads."""

from __future__ import annotations

import logging
from typing import Any

from supabase import Client, create_client

from app.config import settings
from app.schemas import AuditInput, AuditResult, LeadInput

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Client factory
# ---------------------------------------------------------------------------

_client: Client | None = None


def get_supabase_client() -> Client | None:
    """Return a cached Supabase client, or ``None`` if credentials are missing.

    This allows the app to run (e.g. for local dev / tests) even when
    Supabase is not configured.
    """
    global _client  # noqa: PLW0603

    if _client is not None:
        return _client

    if not settings.supabase_url or not settings.supabase_service_role_key:
        logger.warning("Supabase credentials not configured — DB operations will be skipped.")
        return None

    _client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    return _client


# ---------------------------------------------------------------------------
# Audit CRUD
# ---------------------------------------------------------------------------


async def store_audit(
    public_id: str,
    audit_input: AuditInput,
    audit_result: AuditResult,
) -> dict[str, Any] | None:
    """Persist an audit to the ``audits`` table.

    Returns the inserted row dict on success, ``None`` if Supabase is
    unavailable.
    """
    client = get_supabase_client()
    if client is None:
        logger.info("Supabase not configured — skipping audit storage.")
        return None

    row = {
        "public_id": public_id,
        "team_size": audit_input.team_size,
        "primary_use_case": audit_input.primary_use_case.value,
        "total_monthly_spend": audit_result.total_monthly_spend,
        "total_estimated_savings": audit_result.total_estimated_monthly_savings,
        "overspend_score": audit_result.overspend_score,
        "audit_json": audit_result.model_dump(mode="json"),
    }

    try:
        response = client.table("audits").insert(row).execute()
        logger.info("Stored audit %s", public_id)
        return response.data[0] if response.data else row
    except Exception:
        logger.exception("Failed to store audit %s", public_id)
        return None


async def get_audit_by_public_id(public_id: str) -> dict[str, Any] | None:
    """Fetch a single audit row by its ``public_id``.

    Returns the row dict or ``None`` if not found / Supabase unavailable.
    """
    client = get_supabase_client()
    if client is None:
        return None

    try:
        response = (
            client.table("audits")
            .select("*")
            .eq("public_id", public_id)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0]
        return None
    except Exception:
        logger.exception("Failed to fetch audit %s", public_id)
        return None


# ---------------------------------------------------------------------------
# Lead CRUD
# ---------------------------------------------------------------------------


async def store_lead(lead: LeadInput) -> dict[str, Any] | None:
    """Persist a lead to the ``leads`` table.

    If ``lead.audit_id`` (a public_id) is provided, we look up the
    internal UUID from the audits table and store it as ``audit_uuid``.
    """
    client = get_supabase_client()
    if client is None:
        logger.info("Supabase not configured — skipping lead storage.")
        return None

    # Resolve audit UUID from public_id if provided
    audit_uuid: str | None = None
    if lead.audit_id:
        try:
            resp = (
                client.table("audits")
                .select("id")
                .eq("public_id", lead.audit_id)
                .limit(1)
                .execute()
            )
            if resp.data:
                audit_uuid = resp.data[0]["id"]
        except Exception:
            logger.warning("Could not resolve audit_id %s to UUID", lead.audit_id)

    row: dict[str, Any] = {
        "email": lead.email,
        "company_name": lead.company_name,
        "role": lead.role,
        "team_size": lead.team_size,
    }
    if audit_uuid:
        row["audit_id"] = audit_uuid

    try:
        response = client.table("leads").insert(row).execute()
        logger.info("Stored lead %s", lead.email)
        return response.data[0] if response.data else row
    except Exception:
        logger.exception("Failed to store lead %s", lead.email)
        return None
