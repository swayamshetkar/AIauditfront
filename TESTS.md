# Tests

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

To run a single test file:

```bash
pytest tests/test_workflow_mismatch.py -v
```

To run with coverage:

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

## Test Files

| File | Covers | Tests |
|------|--------|-------|
| `tests/conftest.py` | Shared fixtures (ToolUsage, AuditInput) | — |
| `tests/test_workflow_mismatch.py` | Workflow-mismatch rule: flags tools that don't match the team's primary use case | 5 |
| `tests/test_enterprise_overkill.py` | Enterprise-overkill rule: flags small teams on over-priced enterprise plans | 4 |
| `tests/test_redundancy.py` | Redundancy rule: flags teams running multiple tools in the same category | 4 |
| `tests/test_api_overspend.py` | API-overspend rule: flags disproportionately high per-developer API spend | 3 |
| `tests/test_savings_calculation.py` | Savings invariants: annual = monthly × 12, totals correct, never negative, never exceeds spend | 5 |
| `tests/test_audit_engine.py` | Integration: full audit pipeline, scoring, edge cases | 6 |
| `tests/test_api.py` | FastAPI HTTP layer: health check, POST /api/audit, validation errors | 6 |

**Total: 33 tests across 7 test files.**

## Fixture Overview

All shared fixtures live in `tests/conftest.py`:

| Fixture | Description |
|---------|-------------|
| `cursor_pro_tool` | Single Cursor Pro seat ($20/mo) |
| `cursor_business_tool` | Cursor Teams — 3 seats ($120/mo) |
| `copilot_enterprise_tool` | GitHub Copilot Enterprise — 5 seats ($195/mo) |
| `claude_team_tool` | Claude Team Standard — 5 seats ($125/mo) |
| `chatgpt_plus_tool` | ChatGPT Plus — 1 seat ($20/mo) |
| `openai_api_tool` | OpenAI API pay-as-you-go ($500/mo) |
| `small_writing_team_input` | 3-person writing team with Cursor + ChatGPT |
| `solo_coding_input` | Solo dev with Cursor Pro |
| `large_coding_team_input` | 50-person coding team with enterprise tools |
| `bloated_stack_input` | 5-person team with 6 overlapping tools |

## CI

Tests run automatically on every push and PR to `main` via GitHub Actions. See `.github/workflows/ci.yml`.
