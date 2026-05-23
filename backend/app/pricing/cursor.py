"""Cursor pricing data — verified from https://cursor.com/pricing."""

PRICING: dict[str, dict] = {
    "hobby": {
        "monthly": 0.0,
        "annual_monthly": 0.0,
        "features": [
            "Limited agent requests",
            "Basic completions",
        ],
        "verified_at": "2025-05-21",
        "source": "https://cursor.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "pro": {
        "monthly": 20.0,
        "annual_monthly": 16.0,
        "features": [
            "Unlimited completions",
            "$20 credit pool for premium models",
        ],
        "verified_at": "2025-05-21",
        "source": "https://cursor.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "pro_plus": {
        "monthly": 60.0,
        "annual_monthly": 48.0,
        "features": [
            "Unlimited completions",
            "3x credit pool ($60)",
        ],
        "verified_at": "2025-05-21",
        "source": "https://cursor.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "ultra": {
        "monthly": 200.0,
        "annual_monthly": 160.0,
        "features": [
            "Unlimited completions",
            "20x credit pool ($400)",
        ],
        "verified_at": "2025-05-21",
        "source": "https://cursor.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "teams": {
        "monthly": 40.0,
        "annual_monthly": 32.0,
        "features": [
            "Admin controls",
            "SSO",
            "Centralized billing",
            "Unlimited completions",
        ],
        "verified_at": "2025-05-21",
        "source": "https://cursor.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
    "enterprise": {
        "monthly": None,
        "annual_monthly": None,
        "features": [
            "SCIM provisioning",
            "Audit logs",
            "Custom contracts",
            "Dedicated support",
        ],
        "verified_at": "2025-05-21",
        "source": "https://cursor.com/pricing",
        "max_seats": None,
        "min_seats": None,
    },
}
