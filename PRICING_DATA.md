# Pricing Data

> All pricing verified **2025-05-21**. Prices are in USD. "Custom" means contact-sales pricing that varies by deal.

---

## Cursor

| Plan | Price | Notes |
|------|-------|-------|
| Hobby | Free | Limited completions |
| Pro | $20/user/month | Unlimited completions, GPT-4/Claude |
| Pro+ | $60/user/month | Priority models, higher limits |
| Ultra | $200/user/month | Maximum limits |
| Teams | $40/seat/month | Admin dashboard, team analytics |
| Enterprise | Custom | SSO, SAML, audit logs |

🔗 https://cursor.com/pricing

---

## GitHub Copilot

| Plan | Price | Notes |
|------|-------|-------|
| Free | Free | 2,000 completions/mo |
| Pro | $10/user/month | Unlimited completions |
| Pro+ | $39/user/month | Premium models (Claude, GPT-4o) |
| Business | $19/seat/month | Org management, policy controls |
| Enterprise | $39/seat/month | Fine-tuning, knowledge bases, SSO |

🔗 https://github.com/features/copilot

---

## Claude (Anthropic)

| Plan | Price | Notes |
|------|-------|-------|
| Free | Free | Limited messages |
| Pro | $20/user/month | 5× more usage than Free |
| Max 5× | $100/user/month | 5× more usage than Pro |
| Max 20× | $200/user/month | 20× more usage than Pro |
| Team Standard | $25/seat/month | Min 5 seats, admin console |
| Team Premium | $125/seat/month | Higher limits, priority |
| Enterprise | Custom | SSO, SCIM, data retention controls |

🔗 https://www.anthropic.com/pricing

---

## ChatGPT (OpenAI)

| Plan | Price | Notes |
|------|-------|-------|
| Free | Free | GPT-4o-mini |
| Plus | $20/user/month | GPT-4o, DALL-E, browsing |
| Pro | $200/user/month | Unlimited GPT-4o, o1 |
| Business | $25/seat/month | Admin console, no training on data |
| Enterprise | Custom | SSO, unlimited GPT-4o, data privacy |

🔗 https://openai.com/chatgpt/pricing

---

## Gemini (Google)

| Plan | Price | Notes |
|------|-------|-------|
| Free | Free | Gemini with limited features |
| AI Plus | $7.99/month | Part of Google One AI Plus |
| AI Pro | $19.99/month | Gemini Advanced, 2TB storage |
| AI Ultra 100 | $99.99/month | Highest tier models |
| AI Ultra 200 | $199.99/month | Maximum context + features |

🔗 https://one.google.com/about/plans

---

## Windsurf (Codeium)

| Plan | Price | Notes |
|------|-------|-------|
| Free | Free | Limited completions |
| Pro | $20/user/month | Unlimited completions |
| Teams | $40/seat/month | Team management, analytics |
| Max | $200/user/month | Premium models, max limits |
| Enterprise | $60+/seat/month | SSO, SAML, on-prem option |

🔗 https://windsurf.com/pricing

---

## OpenAI API

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| GPT-4.1 | $2.00/1M tokens | $8.00/1M tokens | Flagship |
| GPT-4.1-mini | $0.40/1M tokens | $1.60/1M tokens | Cost-efficient |
| GPT-4.1-nano | $0.10/1M tokens | $0.40/1M tokens | Fastest/cheapest |

🔗 https://openai.com/api/pricing

---

## Anthropic API

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| Claude Sonnet 4 | $3.00/1M tokens | $15.00/1M tokens | Best balance |
| Claude Opus 4 | $5.00/1M tokens | $25.00/1M tokens | Highest capability |
| Claude Haiku 3.5 | $1.00/1M tokens | $5.00/1M tokens | Fast/cheap |

🔗 https://www.anthropic.com/pricing

---

## Gemini API (Google)

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| Gemini Pro | $1.25/1M tokens | $10.00/1M tokens | Best capability |
| Gemini Flash | $0.15/1M tokens | $0.60/1M tokens | Fast |
| Gemini Flash-Lite | $0.02/1M tokens | $0.10/1M tokens | Cheapest |

🔗 https://ai.google.dev/pricing

---

## How We Use This Data

The audit engine uses these prices to:

1. **Detect enterprise overkill** — compare per-seat cost against cheaper tiers
2. **Calculate potential savings** — estimate the delta if the team downgrades
3. **Benchmark API spend** — flag per-developer API costs that exceed typical ranges
4. **Identify redundancy cost** — sum overlapping tool costs to quantify waste

Prices are hardcoded in `app/engine/pricing.py` and should be reviewed quarterly.
