---
title: Spend Node
emoji: 🐢
colorFrom: yellow
colorTo: indigo
sdk: docker
pinned: false
---

# Spend Node by Credex — Cloud Infrastructure & AI Liquidity Engine

> Unlock liquidity from unused cloud credits or access verified compute at a fraction of the cost.

Spend Node analyzes your team's AI tool and cloud subscriptions — Cursor, Copilot, ChatGPT, Claude, and more — and identifies redundancy, enterprise overkill, workflow mismatches, and API overspend. Teams typically discover **$200–$2,000/month** in savings they didn't know they were leaving on the table.

### 🌐 Live Demo
🔗 **Frontend (Next.js):** [https://a-iauditfront.vercel.app](https://a-iauditfront.vercel.app)

---

## Architecture & Backend Logic

This project operates as a **Fullstack Monorepo**.
- **Frontend (Root):** A sleek Next.js React application styled with TailwindCSS and Framer Motion, utilizing the "Blueprint" design system. It captures user inputs and renders the gated audit flow.
- **Backend (`/backend`):** A robust Python FastAPI backend powered by a deterministic, rule-based audit engine.

### How the Engine Analyzes Tools

The backend uses a **Universal Mathematical Scoring Model** paired with a deterministic rule engine.

#### 1. The Universal Curve
Instead of using rigid "point deductions," the engine dynamically calculates the *Optimal Spend* for any given team size and stack composition. It then calculates the ratio `R = actual_spend / optimal_spend` and maps it to a 0-100 score using a continuous asymptote curve.
This creates a robust **Dual Penalty System**:
- **Extreme Overspend (The Waste Ratio):** If a user inputs $66,000,000 for a $100 optimal stack, the curve detects 99.99% waste and crushes the score to exactly `0/100`.
- **Extreme Under-utilization (Adoption Deficit):** If a user inputs a $1 spend for a 10,000 person team, the curve detects massive AI starvation and instantly crashes the score to `0/100`.

This means the math inherently solves for *every numerical permutation from zero to infinity*.

#### 2. The Textual Insights Engine
While the curve governs the math, the tools are grouped into strict categories (`coding`, `productivity`, `api`) and evaluated against specific rules to generate the *Why* in English:

| Rule | Description | Target Comparison |
| :--- | :--- | :--- |
| **Workflow Mismatch** | Flags tools being used by the wrong roles. | Flags coding tools (Cursor, Copilot) if the primary team use-case is non-technical (e.g., Marketing). |
| **Enterprise Overkill** | Flags excessive spending on premium plans. | Flags expensive enterprise tiers (e.g., ChatGPT Enterprise) if the team size is too small to benefit. |
| **Redundancy** | Flags overlapping subscriptions. | Compares tools in the same category. For example, if a team has both **Cursor** and **Copilot**, it recommends dropping the more expensive one. It does the same for overlapping productivity tools (e.g., **ChatGPT Plus** and **Claude Pro**). |
| **API Overspend** | Flags inefficient seat-based spending. | Analyzes total seat cost. If seat costs exceed typical API consumption costs, it recommends shifting to API access (OpenAI API, Anthropic API) with internal UIs. |
| **Seat Efficiency** | Flags unused seats. | Compares `team_size` against `total_seats`. Recommends canceling seats that exceed headcount. |
| **Adoption Deficit** | Flags AI starvation. | Triggers when the team is severely under-investing in AI relative to their headcount. |

### The Secure Gate & Security Measures

We treat cloud infrastructure and spending data as highly sensitive. To prevent audit data from leaking in browser DevTools or via scraping, the backend implements a **Zero-Trust 2-Step Flow**:

1. **Gated Preview (`POST /api/audit-preview`):**
   - The frontend submits the raw data. The engine runs, but *only* returns the high-level efficiency score and dollar amounts. The detailed breakdown is immediately discarded from memory, ensuring it never touches the client's browser.
2. **Secure Generation (`POST /api/audit-and-send`):**
   - When the user provides their email, the engine re-runs the full report. 
   - It generates a cryptographically secure, 12-character URL-safe NanoID (`public_id`) that is mathematically impossible to guess.
   - The data is stored in **Supabase** under this ID.
   - **Resend** is used to securely email a magic link to the user.
3. **Hydration (`GET /api/audit/{public_id}`):** 
   - When the user clicks the email link, this endpoint hydrates the frontend with the private report.
4. **Honeypot Protection:**
   - Lead capture endpoints include hidden "website" fields to catch and silently reject automated bot submissions.

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

---

## License

MIT
