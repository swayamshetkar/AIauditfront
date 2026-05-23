"""Google Gemini pricing data — verified from https://one.google.com/about/plans."""

PRICING: dict[str, dict] = {
    "free": {
        "monthly": 0.0,
        "annual_monthly": 0.0,
        "features": [
            "Basic Gemini access",
            "Limited daily usage",
        ],
        "verified_at": "2025-05-21",
        "source": "https://one.google.com/about/plans",
        "max_seats": None,
        "min_seats": None,
    },
    "ai_plus": {
        "monthly": 7.99,
        "annual_monthly": 7.99,
        "features": [
            "200 GB storage",
            "Gemini Advanced lite access",
        ],
        "verified_at": "2025-05-21",
        "source": "https://one.google.com/about/plans",
        "max_seats": None,
        "min_seats": None,
    },
    "ai_pro": {
        "monthly": 19.99,
        "annual_monthly": 19.99,
        "features": [
            "Expanded Gemini usage",
            "2 TB storage",
            "Advanced features",
        ],
        "verified_at": "2025-05-21",
        "source": "https://one.google.com/about/plans",
        "max_seats": None,
        "min_seats": None,
    },
    "ai_ultra_100": {
        "monthly": 99.99,
        "annual_monthly": 99.99,
        "features": [
            "5x Pro usage limits",
            "Highest model access",
            "30 TB storage",
        ],
        "verified_at": "2025-05-21",
        "source": "https://one.google.com/about/plans",
        "max_seats": None,
        "min_seats": None,
    },
    "ai_ultra_200": {
        "monthly": 199.99,
        "annual_monthly": 199.99,
        "features": [
            "20x Pro usage limits",
            "Highest model access",
            "30 TB storage",
            "Premium support",
        ],
        "verified_at": "2025-05-21",
        "source": "https://one.google.com/about/plans",
        "max_seats": None,
        "min_seats": None,
    },
}
