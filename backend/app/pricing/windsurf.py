"""Windsurf pricing data — verified from https://windsurf.com/pricing."""

PRICING: dict[str, dict] = {
    "free": {
        "monthly": 0.0,
        "annual_monthly": 0.0,
        "features": [
            "Daily quota refresh",
            "Basic completions",
        ],
        "verified_at": "2025-05-21",
        "source": "https://windsurf.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "pro": {
        "monthly": 20.0,
        "annual_monthly": 16.0,
        "features": [
            "Premium model access",
            "Unlimited completions",
            "Advanced flows",
        ],
        "verified_at": "2025-05-21",
        "source": "https://windsurf.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "teams": {
        "monthly": 40.0,
        "annual_monthly": 32.0,
        "features": [
            "Admin dashboard",
            "Centralized billing",
            "Team management",
        ],
        "verified_at": "2025-05-21",
        "source": "https://windsurf.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "max": {
        "monthly": 200.0,
        "annual_monthly": 160.0,
        "features": [
            "Highest quotas",
            "Premium models",
            "Priority support",
        ],
        "verified_at": "2025-05-21",
        "source": "https://windsurf.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "enterprise": {
        "monthly": 60.0,
        "annual_monthly": 60.0,
        "features": [
            "SSO/SAML",
            "Compliance controls",
            "Custom contracts",
            "Dedicated support",
        ],
        "verified_at": "2025-05-21",
        "source": "https://windsurf.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
}
