"""Anthropic API pricing data — verified from https://www.anthropic.com/pricing."""

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
        "source": "https://www.anthropic.com/pricing",
        "models": {
            "claude-sonnet-4": {
                "input_per_1m": 3.00,
                "output_per_1m": 15.00,
            },
            "claude-opus-4": {
                "input_per_1m": 5.00,
                "output_per_1m": 25.00,
            },
            "claude-haiku-3.5": {
                "input_per_1m": 1.00,
                "output_per_1m": 5.00,
            },
        },
    },
}
