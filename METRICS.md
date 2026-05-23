# Metrics

## North Star Metric

**Monthly Estimated Savings Delivered** — the total dollar amount of savings identified across all audits completed in a given month.

**Why this metric?**

- Directly measures the value we create for users
- Correlates with willingness to pay (more savings → higher perceived value)
- Grows with both *volume* (more audits) and *quality* (better recommendations)
- Easy to calculate from existing data: `SUM(total_estimated_monthly_savings)` across all audits

**Target**: $500K/month in identified savings within 6 months of launch.

---

## Input Metrics

These three metrics drive the North Star:

### 1. Completed Audits per Week

**Definition**: Number of audits that reach the results page (not abandoned mid-form).

**Why it matters**: More audits = more savings identified. This is the volume lever.

**Target**: 500 audits/week by Week 8.

**How to move it**:
- Reduce form friction (fewer fields, smarter defaults)
- SEO + content marketing for organic traffic
- Community launches (Show HN, Reddit, Twitter)

### 2. Average Savings per Audit

**Definition**: Mean `total_estimated_monthly_savings` across all completed audits.

**Why it matters**: This is the quality lever — are our rules finding real, significant issues?

**Target**: $150/mo average savings per audit.

**How to move it**:
- Improve rule accuracy (reduce false positives)
- Add new rules (seat waste, plan optimization)
- Better pricing data (more granular tier comparisons)

### 3. Email Capture Rate

**Definition**: % of completed audits where the user provides an email address.

**Why it matters**: Email = lead = potential paying customer. This is the monetization lever.

**Target**: 30% capture rate.

**How to move it**:
- Offer PDF report as incentive
- Promise quarterly re-audit notifications
- Show "compare with similar teams" as gated content

---

## Instrumentation Priority

What to instrument first, in order:

| Priority | Event | Properties | Why |
|----------|-------|------------|-----|
| P0 | `audit.completed` | `team_size`, `tool_count`, `overspend_score`, `total_savings`, `use_case` | Core funnel metric |
| P0 | `audit.started` | `source`, `referrer` | Measure drop-off from start → complete |
| P1 | `email.captured` | `audit_id`, `has_company` | Monetization funnel |
| P1 | `recommendation.viewed` | `rule_name`, `severity`, `tool` | Which recommendations do users care about? |
| P2 | `audit.shared` | `audit_id`, `share_method` | Virality signal |
| P2 | `page.viewed` | `path`, `referrer`, `time_on_page` | Basic web analytics |
| P3 | `api.error` | `endpoint`, `status_code`, `error` | Reliability monitoring |

### Implementation

- **P0 events**: Instrument in Week 1, before launch
- **P1 events**: Instrument in Week 2, alongside email capture feature
- **P2–P3 events**: Instrument in Week 3–4, as features ship

**Stack**: PostHog (free tier, self-hostable, privacy-friendly) or Mixpanel (better funnels, more expensive).

---

## Pivot Triggers

Clear, pre-committed signals that the current approach isn't working:

| Signal | Threshold | Timeline | Action |
|--------|-----------|----------|--------|
| Completed audits | < 50 total | After 3 weeks of active distribution | Problem isn't painful enough. Pivot to usage monitoring (track actual AI tool usage, not just spend). |
| Average savings | < $50/mo per audit | After 100 audits | Rules aren't finding real issues. Either the pricing data is wrong or the rules are too conservative. Deep-dive into false negatives. |
| Email capture rate | < 10% | After 200 audits | Users don't value the result enough to give email. Either the audit output isn't compelling or the incentive is wrong. A/B test the post-audit CTA. |
| Paid conversion | < 1% of email leads | After 50 leads | Free audit is "good enough." Either gate more features or pivot to a different revenue model (consulting, enterprise contracts). |
| NPS / qualitative | Majority of feedback is "interesting but I wouldn't change anything" | After 10 user conversations | Tool is informational, not actionable. Need to close the loop (automate the changes, integrate with billing systems). |

**Rule**: If 2+ pivot triggers fire simultaneously, convene a strategy discussion within 48 hours. Don't wait for all signals to turn red.
