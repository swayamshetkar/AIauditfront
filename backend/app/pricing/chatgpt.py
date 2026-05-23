"""ChatGPT (OpenAI) pricing data — verified from https://openai.com/chatgpt/pricing."""

PRICING: dict[str, dict] = {
    "free": {
        "monthly": 0.0,
        "annual_monthly": 0.0,
        "features": [
            "Basic access to GPT models",
            "Limited usage",
        ],
        "verified_at": "2025-05-21",
        "source": "https://openai.com/chatgpt/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "plus": {
        "monthly": 20.0,
        "annual_monthly": 16.0,
        "features": [
            "GPT-4.5 and GPT-5 access",
            "Deep research",
            "Advanced voice mode",
        ],
        "verified_at": "2025-05-21",
        "source": "https://openai.com/chatgpt/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "pro": {
        "monthly": 200.0,
        "annual_monthly": 200.0,
        "features": [
            "20x Plus usage limits",
            "1M context window",
            "Highest model access",
            "Priority access",
        ],
        "verified_at": "2025-05-21",
        "source": "https://openai.com/chatgpt/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "business": {
        "monthly": 25.0,
        "annual_monthly": 20.0,
        "features": [
            "Workspace management",
            "SSO",
            "Admin console",
            "Data excluded from training",
        ],
        "verified_at": "2025-05-21",
        "source": "https://openai.com/chatgpt/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "enterprise": {
        "monthly": None,
        "annual_monthly": None,
        "features": [
            "Custom pricing (150+ seats)",
            "Dedicated support",
            "Custom data retention",
            "Advanced analytics",
        ],
        "verified_at": "2025-05-21",
        "source": "https://openai.com/chatgpt/pricing",
        "max_seats": None,
        "min_seats": 150,
    },
}
