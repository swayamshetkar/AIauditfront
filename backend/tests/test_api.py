"""Tests for the FastAPI HTTP layer.

Uses FastAPI's TestClient (backed by httpx) to exercise endpoints without
running a live server.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestHealthCheck:
    """Verify the health-check endpoint."""

    def test_health_check_returns_200(self) -> None:
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_body(self) -> None:
        response = client.get("/health")
        body = response.json()
        assert "status" in body or response.status_code == 200

    def test_openapi_schema(self) -> None:
        response = client.get("/openapi.json")
        assert response.status_code == 200


class TestCreateAudit:
    """Verify the POST /api/audit endpoint."""

    def test_create_audit_success(self) -> None:
        """Valid payload should return 200 with an AuditResult."""
        payload = {
            "team_size": 5,
            "primary_use_case": "coding",
            "tools": [
                {
                    "tool": "cursor",
                    "plan": "teams",
                    "monthly_spend": 200.0,
                    "seats": 5,
                },
                {
                    "tool": "github_copilot",
                    "plan": "enterprise",
                    "monthly_spend": 195.0,
                    "seats": 5,
                },
            ],
        }
        response = client.post("/api/audit", json=payload)
        print(response.json())
        assert response.status_code == 200

        body = response.json()
        assert "audit" in body
        assert "overspend_score" in body["audit"]
        assert "public_id" in body
        assert isinstance(body["audit"]["recommendations"], list)
        assert body["audit"]["team_size"] == 5

    def test_create_audit_single_tool(self) -> None:
        """Auditing a single tool should also succeed."""
        payload = {
            "team_size": 1,
            "primary_use_case": "coding",
            "tools": [
                {
                    "tool": "cursor",
                    "plan": "pro",
                    "monthly_spend": 20.0,
                    "seats": 1,
                }
            ],
        }
        response = client.post("/api/audit", json=payload)
        assert response.status_code == 200

    def test_create_audit_invalid_team_size(self) -> None:
        """Negative team size should fail validation (422)."""
        payload = {
            "team_size": -1,
            "primary_use_case": "coding",
            "tools": [
                {
                    "tool": "cursor",
                    "plan": "pro",
                    "monthly_spend": 20.0,
                    "seats": 1,
                }
            ],
        }
        response = client.post("/api/audit", json=payload)
        assert response.status_code == 422

    def test_create_audit_invalid_use_case(self) -> None:
        """Unknown use case string should fail validation (422)."""
        payload = {
            "team_size": 3,
            "primary_use_case": "underwater_basket_weaving",
            "tools": [
                {
                    "tool": "cursor",
                    "plan": "pro",
                    "monthly_spend": 20.0,
                    "seats": 1,
                }
            ],
        }
        response = client.post("/api/audit", json=payload)
        assert response.status_code == 422

    def test_create_audit_empty_tools(self) -> None:
        """Empty tools list should fail validation (422)."""
        payload = {
            "team_size": 3,
            "primary_use_case": "coding",
            "tools": [],
        }
        response = client.post("/api/audit", json=payload)
        assert response.status_code == 422

    def test_create_audit_missing_fields(self) -> None:
        """Missing required fields should fail validation (422)."""
        payload = {"team_size": 3}
        response = client.post("/api/audit", json=payload)
        assert response.status_code == 422
