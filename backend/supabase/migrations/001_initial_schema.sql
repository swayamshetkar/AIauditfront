-- 001_initial_schema.sql
-- AIRev database schema — audits and lead capture
--
-- This migration creates the core tables for persisting audit results
-- and collecting leads from users who want follow-up recommendations.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ──────────────────────────────────────────────────────────────────────
-- audits: stores every completed audit with its full JSON payload
-- ──────────────────────────────────────────────────────────────────────
CREATE TABLE audits (
    id                     UUID          PRIMARY KEY DEFAULT uuid_generate_v4(),
    public_id              TEXT          UNIQUE NOT NULL,
    created_at             TIMESTAMPTZ   DEFAULT NOW(),
    team_size              INTEGER       NOT NULL,
    primary_use_case       TEXT          NOT NULL,
    total_monthly_spend    NUMERIC(10,2) NOT NULL,
    total_estimated_savings NUMERIC(10,2) NOT NULL,
    overspend_score        INTEGER       NOT NULL CHECK (overspend_score >= 0 AND overspend_score <= 100),
    audit_json             JSONB         NOT NULL
);

-- ──────────────────────────────────────────────────────────────────────
-- leads: email + optional metadata, linked to an audit
-- ──────────────────────────────────────────────────────────────────────
CREATE TABLE leads (
    id            UUID          PRIMARY KEY DEFAULT uuid_generate_v4(),
    email         TEXT          NOT NULL,
    company_name  TEXT,
    role          TEXT,
    team_size     INTEGER,
    created_at    TIMESTAMPTZ   DEFAULT NOW(),
    audit_id      UUID          REFERENCES audits(id) ON DELETE SET NULL
);

-- ──────────────────────────────────────────────────────────────────────
-- Indexes
-- ──────────────────────────────────────────────────────────────────────
CREATE INDEX idx_audits_public_id ON audits(public_id);
CREATE INDEX idx_leads_audit_id   ON leads(audit_id);
CREATE INDEX idx_leads_email      ON leads(email);
