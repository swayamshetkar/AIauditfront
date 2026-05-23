"""Pydantic schemas for all input/output validation across the API and engine."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class UseCase(str, Enum):
    """Primary workflow use case for the team."""

    CODING = "coding"
    WRITING = "writing"
    RESEARCH = "research"
    DATA = "data"
    MIXED = "mixed"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ToolCategory(str, Enum):
    CODING = "coding"
    PRODUCTIVITY = "productivity"
    API = "api"


class PricingType(str, Enum):
    SEAT = "seat"
    USAGE = "usage"
    SEAT_PLUS_API = "seat+api"


# ---------------------------------------------------------------------------
# Supported tool names — canonical identifiers
# ---------------------------------------------------------------------------

SUPPORTED_TOOLS = [
    "cursor",
    "github_copilot",
    "windsurf",
    "chatgpt",
    "claude",
    "gemini",
    "openai_api",
    "anthropic_api",
    "gemini_api",
]


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class ToolUsage(BaseModel):
    """A single AI tool the user's team pays for."""

    tool: str = Field(..., description="Canonical tool identifier (e.g. 'cursor', 'claude')")
    plan: str = Field(..., description="Plan name (e.g. 'pro', 'business', 'enterprise')")
    monthly_spend: float = Field(..., gt=0, description="Current monthly spend in USD")
    seats: int | None = Field(default=None, ge=1, description="Number of seats/licenses")

    @model_validator(mode="after")
    def validate_plan_for_tool(self) -> ToolUsage:
        from app.pricing.registry import get_all_plans
        valid_plans = get_all_plans(self.tool)
        # If tool isn't in registry at all, we could also flag it, 
        # but let's just validate the plan if the tool is known.
        if valid_plans and self.plan.lower() not in [p.lower() for p in valid_plans]:
            raise ValueError(f"Invalid plan '{self.plan}' for tool '{self.tool}'. Valid plans are: {', '.join(valid_plans)}")
        return self


class AuditInput(BaseModel):
    """Complete input for an AI spend audit."""

    team_size: int = Field(..., ge=1, le=10000, description="Total team size")
    primary_use_case: UseCase
    tools: list[ToolUsage] = Field(..., min_length=1, max_length=20)


# ---------------------------------------------------------------------------
# Output schemas
# ---------------------------------------------------------------------------


class Recommendation(BaseModel):
    """A single audit recommendation for one tool."""

    tool: str
    severity: Severity
    issue: str
    recommendation: str
    reasoning: str
    estimated_monthly_savings: float = Field(ge=0)
    estimated_annual_savings: float = Field(ge=0)
    confidence: Confidence


class ScoreBreakdown(BaseModel):
    """Breakdown of the overspend score by rule."""

    rule: str
    weight: int
    raw_score: float = Field(ge=0, le=100)
    weighted_score: float


class AuditResult(BaseModel):
    """Complete audit output returned by the engine."""

    overspend_score: int = Field(ge=0, le=100)
    score_label: str
    score_breakdown: list[ScoreBreakdown]
    recommendations: list[Recommendation]
    total_monthly_spend: float
    total_estimated_monthly_savings: float
    total_estimated_annual_savings: float
    tool_count: int
    team_size: int
    primary_use_case: UseCase
    tools_analyzed: list[str]


class AuditResponse(BaseModel):
    """API response wrapping the audit result with metadata."""

    public_id: str
    audit: AuditResult
    created_at: str


class AuditPreviewResponse(BaseModel):
    """API response returning only top-level score and savings (hides detailed recommendations and public_id)."""

    overspend_score: int
    score_label: str
    total_monthly_spend: float
    total_estimated_monthly_savings: float
    total_estimated_annual_savings: float


# ---------------------------------------------------------------------------
# Lead capture schemas
# ---------------------------------------------------------------------------


class LeadInput(BaseModel):
    """Lead capture form submission."""

    email: str = Field(..., min_length=5, max_length=254)
    company_name: str | None = Field(default=None, max_length=200)
    role: str | None = Field(default=None, max_length=100)
    team_size: int | None = Field(default=None, ge=1, le=10000)
    audit_id: str | None = Field(default=None, description="public_id of the associated audit")
    # Honeypot field — must be empty. Bots fill hidden fields.
    website: str | None = Field(default=None, max_length=0)


class GatedAuditInput(AuditInput):
    """Input payload containing both the audit stack and the lead capture details."""

    email: str = Field(..., min_length=5, max_length=254)
    company_name: str | None = Field(default=None, max_length=200)
    role: str | None = Field(default=None, max_length=100)
    website: str | None = Field(default=None, max_length=0)



class LeadResponse(BaseModel):
    success: bool
    message: str


# ---------------------------------------------------------------------------
# AI summary schemas
# ---------------------------------------------------------------------------


class SummaryRequest(BaseModel):
    """Request body for AI summary generation."""

    audit_result: AuditResult


class SummaryResponse(BaseModel):
    summary: str
    source: Literal["ai", "fallback"]
