import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_audit_preview_does_not_leak_details():
    payload = {
        "team_size": 10,
        "primary_use_case": "coding",
        "tools": [
            {"tool": "cursor", "plan": "pro", "monthly_spend": 200, "seats": 10}
        ]
    }

    response = client.post("/api/audit-preview", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Should contain top-level metrics
    assert "overspend_score" in data
    assert "total_estimated_monthly_savings" in data

    # MUST NOT contain public_id or detailed recommendations
    assert "public_id" not in data
    assert "recommendations" not in data
    assert "audit" not in data

@pytest.mark.asyncio
async def test_audit_and_send_success():
    payload = {
        "team_size": 10,
        "primary_use_case": "coding",
        "tools": [
            {"tool": "cursor", "plan": "pro", "monthly_spend": 200, "seats": 10}
        ],
        "email": "test@example.com",
        "company_name": "Test",
        "role": "Engineer",
        "website": ""
    }

    response = client.post("/api/audit-and-send", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Should return only success message
    assert data["success"] is True
    assert "message" in data

    # MUST NOT return public_id or audit object
    assert "public_id" not in data
    assert "audit" not in data
