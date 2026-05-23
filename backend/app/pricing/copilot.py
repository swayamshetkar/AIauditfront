"""GitHub Copilot pricing data — verified from https://github.com/features/copilot."""

PRICING: dict[str, dict] = {
    "free": {
        "monthly": 0.0,
        "annual_monthly": 0.0,
        "features": [
            "Limited ~2000 completions/month",
            "Basic code suggestions",
        ],
        "verified_at": "2025-05-21",
        "source": "https://github.com/features/copilot",
        "max_seats": None,
        "min_seats": None,
    },
    "pro": {
        "monthly": 10.0,
        "annual_monthly": 10.0,
        "features": [
            "Unlimited completions",
            "Chat in IDE and mobile",
        ],
        "verified_at": "2025-05-21",
        "source": "https://github.com/features/copilot",
        "max_seats": None,
        "min_seats": None,
    },
    "pro_plus": {
        "monthly": 39.0,
        "annual_monthly": 39.0,
        "features": [
            "Higher premium model credits",
            "Unlimited completions",
            "Agent mode",
        ],
        "verified_at": "2025-05-21",
        "source": "https://github.com/features/copilot",
        "max_seats": None,
        "min_seats": None,
    },
    "business": {
        "monthly": 19.0,
        "annual_monthly": 19.0,
        "features": [
            "Organization-wide controls",
            "SSO/SAML",
            "Policy management",
        ],
        "verified_at": "2025-05-21",
        "source": "https://github.com/features/copilot",
        "max_seats": None,
        "min_seats": None,
    },
    "enterprise": {
        "monthly": 39.0,
        "annual_monthly": 39.0,
        "features": [
            "Knowledge bases",
            "Fine-tuned models",
            "Requires GitHub Enterprise Cloud",
            "Advanced security",
        ],
        "verified_at": "2025-05-21",
        "source": "https://github.com/features/copilot",
        "max_seats": None,
        "min_seats": None,
    },
}
