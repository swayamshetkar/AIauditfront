"""Google AI Studio (Gemini API) pricing data — verified from https://ai.google.dev/pricing."""

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
        "source": "https://ai.google.dev/pricing",
        "models": {
            "gemini-2.5-pro": {
                "input_per_1m": 1.25,
                "output_per_1m": 10.00,
            },
            "gemini-2.5-flash": {
                "input_per_1m": 0.15,
                "output_per_1m": 0.60,
            },
            "gemini-2.5-flash-lite": {
                "input_per_1m": 0.02,
                "output_per_1m": 0.10,
            },
        },
    },
}
