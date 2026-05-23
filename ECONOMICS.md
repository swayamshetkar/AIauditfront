# Unit Economics

## The AIRev Business Model

AIRev operates as a **freemium SaaS** with a free audit tier and a paid tier for ongoing monitoring, team dashboards, and priority support. Here's the math.

---

## Revenue Model

| Tier | Price | What You Get |
|------|-------|-------------|
| Free | $0 | One-time audit, shareable results URL |
| Pro | $49/mo per team | Quarterly re-audits, PDF reports, email alerts on pricing changes, usage recommendations |
| Enterprise | $199/mo per team | Everything in Pro + SSO, custom rules, Slack integration, dedicated support |

---

## Cost Structure (Per Audit)

| Cost Item | Per Audit | Notes |
|-----------|-----------|-------|
| **Compute (FastAPI)** | ~$0.001 | Rule engine is CPU-only, ~10ms per audit |
| **AI Summary (Claude Sonnet 4)** | ~$0.015 | ~800 input tokens + ~500 output tokens at $3/$15 per 1M |
| **Database (Supabase)** | ~$0.0001 | ~2KB per audit, well within free tier |
| **Email (Resend)** | ~$0.001 | Only if lead capture email is sent |
| **Total COGS per audit** | **~$0.017** | |

At scale (10K audits/month):
- Compute: ~$50/mo (Railway or Fly.io)
- AI Summaries: ~$150/mo
- Database: $25/mo (Supabase Pro)
- Email: $20/mo (Resend)
- **Total infrastructure: ~$245/mo**

---

## Unit Economics at Scale

### Assumptions

- 10,000 free audits/month
- 3% conversion to Pro ($49/mo) = 300 Pro teams
- 0.3% conversion to Enterprise ($199/mo) = 30 Enterprise teams
- Monthly churn: 5% (Pro), 3% (Enterprise)

### Monthly Revenue

```
Pro:        300 teams × $49/mo  = $14,700/mo
Enterprise:  30 teams × $199/mo =  $5,970/mo
────────────────────────────────────────────
Total MRR:                        $20,670/mo
```

### Monthly Costs

```
Infrastructure:                     $245/mo
AI API costs (summaries):           $150/mo
Resend (email):                      $20/mo
Domain + misc:                       $30/mo
────────────────────────────────────────────
Total COGS:                         $445/mo
```

### Gross Margin

```
Gross Profit:  $20,670 - $445 = $20,225/mo
Gross Margin:  $20,225 / $20,670 = 97.8%
```

This is typical for SaaS with minimal per-unit compute costs. The margin will compress slightly at higher scale (more AI summary calls, database upgrades), but should stay above 90%.

---

## Customer Acquisition Cost (CAC)

### Organic (SEO + Community)

- Cost: ~$0 (time investment, no ad spend)
- Conversion: 10,000 audits → 330 paid teams
- **Effective CAC: ~$0** (excluding founder time)

### LinkedIn Outbound

- Tools: LinkedIn Sales Navigator ($99/mo) + email automation ($50/mo)
- Volume: 400 messages/mo × 3% response × 50% close = 6 customers/mo
- **CAC: $149/mo ÷ 6 = ~$25/customer**

### Paid Ads (Future)

- Estimated: $5–$15 CPC on Google Ads for "AI tool spending" keywords
- Conversion funnel: 100 clicks → 30 audits → 1 paid team
- **CAC: $500–$1,500/customer** (only viable at scale with proven LTV)

---

## Lifetime Value (LTV)

### Pro Tier

```
ARPU:          $49/mo
Avg lifetime:  1 / 5% churn = 20 months
LTV:           $49 × 20 = $980
```

### Enterprise Tier

```
ARPU:          $199/mo
Avg lifetime:  1 / 3% churn = 33 months
LTV:           $199 × 33 = $6,567
```

### Blended LTV

```
(300 × $980 + 30 × $6,567) / 330 = $1,488
```

---

## LTV:CAC Ratio

| Channel | CAC | LTV | LTV:CAC |
|---------|-----|-----|---------|
| Organic | ~$0 | $1,488 | ∞ |
| LinkedIn Outbound | $25 | $1,488 | 59:1 |
| Paid Ads (est.) | $500–$1,500 | $1,488 | 1–3:1 |

**Target**: LTV:CAC > 3:1 for healthy SaaS economics. Organic and outbound are excellent; paid ads need careful optimization.

---

## Break-Even Analysis

With founder-only operation (no salary cost):

```
Fixed costs:    ~$445/mo (infrastructure)
Revenue needed: $445/mo ÷ 97.8% margin = ~$455/mo
Break-even:     10 Pro customers ($490/mo)
```

**We break even at 10 paying customers.** This is achievable within the first month of active distribution.

---

## Key Risks to the Model

1. **AI summary costs could spike** if usage patterns change (longer reports, more re-audits). Mitigation: cache common patterns, use cheaper models for simple audits.
2. **Churn could be higher than 5%** if the audit is a "one-and-done" value prop. Mitigation: add ongoing monitoring and alerts that create recurring value.
3. **Free tier could cannibalize paid** if the one-time audit is "good enough." Mitigation: withhold PDF export, quarterly re-audits, and team features behind the paywall.
