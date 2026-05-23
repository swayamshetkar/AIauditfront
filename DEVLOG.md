# Development Log

## Day 1 — 2025-05-21 (Wednesday)

### What I Built

- Initialized the Python project structure: `app/`, `tests/`, `supabase/migrations/`
- Defined all Pydantic schemas in `app/schemas.py`: `UseCase`, `Severity`, `Confidence`, `ToolUsage`, `AuditInput`, `Recommendation`, `AuditResult`
- Set up FastAPI app skeleton in `app/main.py` with `/health` and `/api/audit` endpoints
- Created the rule engine architecture: `app/engine/rules/` with a consistent interface (`RULE_NAME`, `RULE_WEIGHT`, `evaluate()`)
- Wrote the initial database migration (`001_initial_schema.sql`) for Supabase
- Built the full test suite: 33 tests across 7 files covering every rule, integration, and API layer
- Set up CI with GitHub Actions (lint + test on every push/PR)
- Collected and verified pricing data for 9 AI tools/APIs

### Decisions Made

1. **Rule-based engine** over ML — interpretability and debuggability matter more than sophistication at this stage
2. **Per-tool evaluation** with `all_tools` context — keeps rules modular while enabling cross-tool analysis
3. **Weighted scoring (0–100)** — more useful than binary "has issues" / "no issues"
4. **Supabase for persistence** — free tier is sufficient for MVP, standard Postgres underneath
5. **Python 3.11+ with strict typing** — type hints everywhere, catches bugs before runtime

### Blockers

- None today. Clean start.

### Tomorrow's Plan

- Implement the first two rules: `workflow_mismatch` and `enterprise_overkill`
- Get the audit engine returning real recommendations
- Make the test suite pass end-to-end

---

## Day 2 — 2025-05-22 (Thursday)

### What I Built

<!-- TODO: Fill in -->

### Decisions Made

<!-- TODO: Fill in -->

### Blockers

<!-- TODO: Fill in -->

### Tomorrow's Plan

<!-- TODO: Fill in -->

---

## Day 3 — 2025-05-23 (Friday)

### What I Built

<!-- TODO: Fill in -->

### Decisions Made

<!-- TODO: Fill in -->

### Blockers

<!-- TODO: Fill in -->

### Tomorrow's Plan

<!-- TODO: Fill in -->

---

## Day 4 — 2025-05-24 (Saturday)

### What I Built

<!-- TODO: Fill in -->

### Decisions Made

<!-- TODO: Fill in -->

### Blockers

<!-- TODO: Fill in -->

### Tomorrow's Plan

<!-- TODO: Fill in -->

---

## Day 5 — 2025-05-25 (Sunday)

### What I Built

<!-- TODO: Fill in -->

### Decisions Made

<!-- TODO: Fill in -->

### Blockers

<!-- TODO: Fill in -->

### Tomorrow's Plan

<!-- TODO: Fill in -->

---

## Day 6 — 2025-05-26 (Monday)

### What I Built

<!-- TODO: Fill in -->

### Decisions Made

<!-- TODO: Fill in -->

### Blockers

<!-- TODO: Fill in -->

### Tomorrow's Plan

<!-- TODO: Fill in -->

---

## Day 7 — 2025-05-27 (Tuesday)

### What I Built

<!-- TODO: Fill in -->

### Decisions Made

<!-- TODO: Fill in -->

### Final Reflection

<!-- TODO: Fill in — link to REFLECTION.md -->
