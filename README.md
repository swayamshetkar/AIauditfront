---
title: AI Audit
emoji: 🐢
colorFrom: yellow
colorTo: indigo
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# AIRev — AI Tool Spending Auditor

> Stop overpaying for AI tools. Get a free audit of your team's AI stack in 60 seconds.

AIRev analyzes your team's AI tool subscriptions — Cursor, Copilot, ChatGPT, Claude, and more — and identifies redundancy, enterprise overkill, workflow mismatches, and API overspend. Teams typically discover **$200–$2,000/month** in savings they didn't know they were leaving on the table.

### 🌐 Live Demo
🔗 **Frontend (Next.js):** [https://a-iauditfront.vercel.app](https://a-iauditfront.vercel.app)

---

## Architecture & Logic Summary

This project is a **Fullstack Monorepo**.
- **Frontend (Root):** A sleek Next.js React application styled with TailwindCSS and Framer Motion. It captures user inputs and renders the gated audit flow.
- **Backend (`/backend`):** A robust Python FastAPI backend powered by a deterministic, rule-based audit engine.

### How the Logic Works:
1. **The Audit Engine:** When the frontend submits an audit request, the backend runs the data through 5 strict rules:
   - *Workflow Mismatch:* Checks if non-coders are paying for coding tools.
   - *Enterprise Overkill:* Checks if small teams are paying for Enterprise plans.
   - *Redundancy:* Checks if teams are paying for overlapping tools (e.g., both Cursor and Copilot).
   - *API Overspend:* Checks if direct API usage would be cheaper than seat-based subscriptions.
   - *Seat Efficiency:* Checks if the team is paying for unused seats.
2. **The Scoring System:** The rules aggregate to generate an "Efficiency Score" (0-100) and calculate exact dollar amounts for potential monthly/annual savings.
3. **The Secure Gate (Email Logic):** To prevent sensitive audit data from leaking in browser DevTools, the backend utilizes a 2-step process:
   - **Step 1 (`/api/audit-preview`):** Runs the audit but only returns the high-level efficiency score to the frontend.
   - **Step 2 (`/api/audit-and-send`):** Saves the full audit to **Supabase**, generates a secure `public_id`, and uses **Resend** to email the user a private link to their full report.

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Supabase project (free tier works)
- Anthropic or OpenAI API key (for AI summaries)

### Install

```bash
git clone https://github.com/your-org/airevfront.git
cd airevfront

# 1. Install Frontend
npm install

# 2. Install Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### Configure

Create a `.env` file at the project root:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
RESEND_API_KEY=re_...
```

### Run

```bash
# Terminal 1: Frontend
npm run dev

# Terminal 2: Backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

API docs at http://localhost:8000/docs

### Test

```bash
pytest tests/ -v
```

### Lint

```bash
ruff check app/ tests/
```

---

## Deploy

### Railway (Recommended for MVP)

```bash
# Install Railway CLI
railway login
railway init
railway up
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deployed URL

🔗 **Live URL:** [https://a-iauditfront.vercel.app](https://a-iauditfront.vercel.app)

---

## Key Decisions

### 1. Rule-based engine over ML

We chose a deterministic rule engine over ML/statistical models because:
- **Interpretability**: Every recommendation has a clear `reasoning` field that explains *why* — impossible with a black-box model.
- **Debuggability**: When a rule produces a bad recommendation, we can fix the specific rule without retraining.
- **Speed**: Rule evaluation takes ~10ms vs. seconds for model inference.
- **Trust**: Enterprise buyers need to understand why they're being told to change tools. "The model said so" doesn't fly.

### 2. Supabase over raw PostgreSQL

Supabase gives us managed Postgres with a generous free tier, built-in auth (for later), and instant REST APIs. The migration path to raw Postgres is trivial — our schema is standard SQL. We chose this over Firebase/DynamoDB because our data is inherently relational (audits → leads → recommendations).

### 3. Python + FastAPI over Node/TypeScript

The team has deeper Python expertise, and FastAPI's Pydantic integration means our schema definitions serve triple duty: API validation, database serialization, and test fixtures. Node would have been fine, but Python's data-processing ecosystem (if we add analytics later) is stronger.

### 4. Per-tool evaluation with `all_tools` context

Each rule evaluates one tool at a time but receives the full tool list. This keeps rules modular (testable in isolation) while enabling cross-tool analysis (redundancy detection). The alternative — a single `evaluate_all()` function — would have been harder to test and extend.

### 5. Weighted scoring over binary flags

A 0–100 overspend score is more useful than "you have problems" / "you don't." It lets us prioritize recommendations, track improvement over time, and set thresholds for different alert levels. The weights are tunable without code changes (planned: move to config).

---

## Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system diagram and scaling discussion.

## Tests

See [TESTS.md](TESTS.md) for the full test inventory and how to run them.

## Pricing Data

See [PRICING_DATA.md](PRICING_DATA.md) for all tool pricing with sources and verification dates.

---

## License

MIT
