"""GET /api/tools — Return supported tools and their valid plans."""

import logging

from fastapi import APIRouter

from app.pricing.registry import PRICING_REGISTRY

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["tools"])

@router.get("/tools")
async def get_tools() -> dict:
    """Return all supported tools and their available plans.
    
    This endpoint allows the frontend to dynamically build dropdowns
    and validate user inputs before submission.
    """
    tools_data = {}
    for tool_name, plans in PRICING_REGISTRY.items():
        tools_data[tool_name] = {
            "plans": list(plans.keys())
        }

    return {"tools": tools_data}
