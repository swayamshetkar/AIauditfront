# AI Prompts and Architecture

## Why Deterministic Audit Logic is Preferred

The core audit engine is entirely deterministic and rule-based. This architectural decision was made because:
1. **Explainability:** Financial recommendations must be fully explainable. A rule-based system allows us to point to the exact logic that triggered a savings recommendation.
2. **Consistency:** An LLM might calculate savings differently on identical inputs. A deterministic engine guarantees the exact same mathematical output every time.
3. **Defensibility:** For Credex to use this as a lead-generation tool, the underlying math must be bulletproof and defensible to CFOs and engineering managers.

## Why AI is Used for Natural Language Summaries

While the math is deterministic, the presentation benefits greatly from AI. We use a generative AI model purely as a presentation layer because:
1. **Personalization:** An LLM can synthesize discrete data points (e.g., team size, specific tool overlap, dollar amounts) into a cohesive, readable narrative.
2. **Tone:** The AI can adopt a "consultant-style" tone that feels professional and tailored to the user's context.
3. **Synthesis:** Instead of reading a dry JSON output or a strict list of alerts, the user receives a thoughtful executive summary that contextualizes their overspend score.

## Final OpenRouter Prompt

We use OpenRouter (specifically the `deepseek/deepseek-chat` model) to generate these summaries. The prompt is designed to be concise, professional, and financially focused.

```text
You are a financial optimization consultant specializing in AI tool spend for startups and engineering teams.

Generate a concise ~100-word personalized summary paragraph for this AI spend audit.

Audit Details:
- Team size: {team_size}
- Primary use case: {primary_use_case}
- Tools analyzed: {tools}
- Total monthly spend: ${total_monthly_spend:.2f}
- Total potential monthly savings: ${total_monthly_savings:.2f}
- Total potential annual savings: ${total_annual_savings:.2f}
- Overspend score: {overspend_score}/100 ({score_label})
- Key issues: {issues}

Guidelines:
- Be direct and professional, like a CFO advisor
- Lead with the most impactful finding
- Mention specific dollar amounts
- If savings are minimal (<$100/mo), acknowledge the team is spending well
- Do NOT use marketing language or hyperbole
- Do NOT mention Credex or any specific vendor
- End with a forward-looking recommendation
- Do NOT invent metrics, invent savings, or make absolute statements
```

### Prompt Engineering Decisions

| Decision | Reasoning |
|----------|-----------|
| "financial optimization consultant" | Grounds the tone — professional, trustworthy, and finance-oriented |
| "~100-word personalized summary" | Prevents rambling and ensures the summary remains an executive paragraph |
| Strict Constraints | Explicitly forbids hallucinations ("Do NOT invent metrics") and exaggerated claims |
| OpenRouter Provider | Ensures the AI layer remains lightweight, cheap, and easily replaceable with different models |
