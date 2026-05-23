"""OpenAI API pricing data — verified from https://openai.com/api/pricing."""

PRICING: dict[str, dict] = {
    "pay_as_you_go": {
        "monthly": None,
        "annual_monthly": None,
        "features": [
            "Usage-based pricing",
            "Pay per token",
            "No monthly commitment",
        ],
        "verified_at": "2025-05-21",
        "source": "https://openai.com/api/pricing",
        "models": {
            "gpt-4.1": {
                "input_per_1m": 2.00,
                "output_per_1m": 8.00,
            },
            "gpt-4.1-mini": {
                "input_per_1m": 0.40,
                "output_per_1m": 1.60,
            },
            "gpt-4.1-nano": {
                "input_per_1m": 0.10,
                "output_per_1m": 0.40,
            },
            "gpt-4o-mini": {
                "input_per_1m": 0.15,
                "output_per_1m": 0.60,
            },
        },
    },
}
