"""Shared test fixtures for the AIRev test suite."""

import pytest

from app.schemas import AuditInput, ToolUsage, UseCase


@pytest.fixture
def cursor_pro_tool() -> ToolUsage:
    """Single Cursor Pro seat at $20/mo."""
    return ToolUsage(tool="cursor", plan="pro", monthly_spend=20.0, seats=1)


@pytest.fixture
def cursor_business_tool() -> ToolUsage:
    """Cursor Teams plan — 3 seats at $40/seat = $120/mo."""
    return ToolUsage(tool="cursor", plan="teams", monthly_spend=120.0, seats=3)


@pytest.fixture
def copilot_enterprise_tool() -> ToolUsage:
    """GitHub Copilot Enterprise — 5 seats at $39/seat = $195/mo."""
    return ToolUsage(tool="github_copilot", plan="enterprise", monthly_spend=195.0, seats=5)


@pytest.fixture
def claude_team_tool() -> ToolUsage:
    """Claude Team Standard — 5 seats at $25/seat = $125/mo."""
    return ToolUsage(tool="claude", plan="team_standard", monthly_spend=125.0, seats=5)


@pytest.fixture
def chatgpt_plus_tool() -> ToolUsage:
    """ChatGPT Plus — single seat at $20/mo."""
    return ToolUsage(tool="chatgpt", plan="plus", monthly_spend=20.0, seats=1)


@pytest.fixture
def openai_api_tool() -> ToolUsage:
    """OpenAI API — pay-as-you-go at $500/mo."""
    return ToolUsage(tool="openai_api", plan="pay_as_you_go", monthly_spend=500.0)


@pytest.fixture
def small_writing_team_input() -> AuditInput:
    """3-person writing team using Cursor Pro + ChatGPT Plus."""
    return AuditInput(
        team_size=3,
        primary_use_case=UseCase.WRITING,
        tools=[
            ToolUsage(tool="cursor", plan="pro", monthly_spend=60.0, seats=3),
            ToolUsage(tool="chatgpt", plan="plus", monthly_spend=60.0, seats=3),
        ],
    )


@pytest.fixture
def solo_coding_input(cursor_pro_tool: ToolUsage) -> AuditInput:
    """Solo developer using just Cursor Pro."""
    return AuditInput(
        team_size=1,
        primary_use_case=UseCase.CODING,
        tools=[cursor_pro_tool],
    )


@pytest.fixture
def large_coding_team_input() -> AuditInput:
    """50-person coding team with enterprise tools."""
    return AuditInput(
        team_size=50,
        primary_use_case=UseCase.CODING,
        tools=[
            ToolUsage(tool="github_copilot", plan="enterprise", monthly_spend=1950.0, seats=50),
            ToolUsage(tool="cursor", plan="teams", monthly_spend=2000.0, seats=50),
        ],
    )


@pytest.fixture
def bloated_stack_input() -> AuditInput:
    """5-person team with an over-provisioned AI stack."""
    return AuditInput(
        team_size=5,
        primary_use_case=UseCase.CODING,
        tools=[
            ToolUsage(tool="cursor", plan="teams", monthly_spend=200.0, seats=5),
            ToolUsage(tool="github_copilot", plan="enterprise", monthly_spend=195.0, seats=5),
            ToolUsage(tool="windsurf", plan="teams", monthly_spend=200.0, seats=5),
            ToolUsage(tool="chatgpt", plan="business", monthly_spend=125.0, seats=5),
            ToolUsage(tool="claude", plan="team_standard", monthly_spend=125.0, seats=5),
            ToolUsage(tool="openai_api", plan="pay_as_you_go", monthly_spend=2000.0),
        ],
    )
