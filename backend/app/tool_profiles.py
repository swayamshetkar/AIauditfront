"""Tool metadata profiles — strengths, weaknesses, and classification for each AI tool."""

from __future__ import annotations

from dataclasses import dataclass

from app.schemas import PricingType, ToolCategory, UseCase


@dataclass
class ToolProfile:
    display_name: str
    category: ToolCategory
    ideal_use_cases: list[UseCase]
    overlap_tools: list[str]
    pricing_type: PricingType
    enterprise_threshold: int | None
    token_intensity: float
    strengths: list[str]
    weaknesses: list[str]

TOOL_PROFILES: dict[str, ToolProfile] = {
    "cursor": ToolProfile(
        display_name="Cursor",
        category=ToolCategory.CODING,
        ideal_use_cases=[UseCase.CODING],
        overlap_tools=["github_copilot", "windsurf"],
        pricing_type=PricingType.SEAT,
        enterprise_threshold=15,
        token_intensity=1.2,
        strengths=[
            "Best-in-class AI code generation",
            "Deep IDE integration",
            "Multi-model support",
        ],
        weaknesses=[
            "Not useful for non-coding workflows",
            "Credit-based premium model access",
        ],
    ),
    "github_copilot": ToolProfile(
        display_name="GitHub Copilot",
        category=ToolCategory.CODING,
        ideal_use_cases=[UseCase.CODING],
        overlap_tools=["cursor", "windsurf"],
        pricing_type=PricingType.SEAT,
        enterprise_threshold=20,
        token_intensity=1.0,
        strengths=[
            "Native GitHub ecosystem integration",
            "Broad IDE support (VS Code, JetBrains, Neovim)",
            "Strong inline completions",
        ],
        weaknesses=[
            "Less agentic than Cursor/Windsurf",
            "Enterprise plan requires GitHub Enterprise Cloud",
        ],
    ),
    "windsurf": ToolProfile(
        display_name="Windsurf",
        category=ToolCategory.CODING,
        ideal_use_cases=[UseCase.CODING],
        overlap_tools=["cursor", "github_copilot"],
        pricing_type=PricingType.SEAT,
        enterprise_threshold=15,
        token_intensity=1.2,
        strengths=[
            "Agentic coding workflows (Cascade)",
            "Full-project context awareness",
            "Competitive pricing for teams",
        ],
        weaknesses=[
            "Smaller ecosystem vs Copilot/Cursor",
            "Newer product with less market validation",
        ],
    ),
    "chatgpt": ToolProfile(
        display_name="ChatGPT",
        category=ToolCategory.PRODUCTIVITY,
        ideal_use_cases=[UseCase.WRITING, UseCase.MIXED],
        overlap_tools=["claude", "gemini"],
        pricing_type=PricingType.SEAT,
        enterprise_threshold=50,
        token_intensity=0.7,
        strengths=[
            "Versatile general-purpose assistant",
            "Best brand recognition and adoption",
            "Strong at writing, brainstorming, and research",
        ],
        weaknesses=[
            "Enterprise plan requires 150+ seats",
            "Pro tier ($200/mo) is expensive for individuals",
        ],
    ),
    "claude": ToolProfile(
        display_name="Claude",
        category=ToolCategory.PRODUCTIVITY,
        ideal_use_cases=[UseCase.WRITING, UseCase.RESEARCH, UseCase.CODING],
        overlap_tools=["chatgpt", "gemini"],
        pricing_type=PricingType.SEAT,
        enterprise_threshold=30,
        token_intensity=0.8,
        strengths=[
            "Excellent at long-form writing and analysis",
            "200K context window standard",
            "Strong coding capabilities alongside productivity",
        ],
        weaknesses=[
            "Fewer integrations than ChatGPT",
            "Team plans require minimum 5 seats",
        ],
    ),
    "gemini": ToolProfile(
        display_name="Gemini",
        category=ToolCategory.PRODUCTIVITY,
        ideal_use_cases=[UseCase.RESEARCH, UseCase.DATA],
        overlap_tools=["chatgpt", "claude"],
        pricing_type=PricingType.SEAT,
        enterprise_threshold=30,
        token_intensity=0.7,
        strengths=[
            "Deep Google Workspace integration",
            "Strong multimodal capabilities",
            "Competitive consumer pricing tiers",
        ],
        weaknesses=[
            "Less mature enterprise offering",
            "Consumer tiers bundled with Google One storage",
        ],
    ),
    "openai_api": ToolProfile(
        display_name="OpenAI API",
        category=ToolCategory.API,
        ideal_use_cases=[UseCase.CODING, UseCase.DATA],
        overlap_tools=["anthropic_api", "gemini_api"],
        pricing_type=PricingType.USAGE,
        enterprise_threshold=None,
        token_intensity=2.0,
        strengths=[
            "Widest model selection (GPT-4.1, 4o, etc.)",
            "Best developer ecosystem and tooling",
            "Fine-tuning and embeddings support",
        ],
        weaknesses=[
            "Costs scale unpredictably with usage",
            "No fixed monthly budget without usage caps",
        ],
    ),
    "anthropic_api": ToolProfile(
        display_name="Anthropic API",
        category=ToolCategory.API,
        ideal_use_cases=[UseCase.WRITING, UseCase.RESEARCH, UseCase.CODING],
        overlap_tools=["openai_api", "gemini_api"],
        pricing_type=PricingType.USAGE,
        enterprise_threshold=None,
        token_intensity=1.8,
        strengths=[
            "Best-in-class reasoning (Claude Opus 4)",
            "200K+ context windows",
            "Strong safety and alignment guarantees",
        ],
        weaknesses=[
            "Smaller model roster than OpenAI",
            "Higher per-token cost for top-tier models",
        ],
    ),
    "gemini_api": ToolProfile(
        display_name="Gemini API (Google AI Studio)",
        category=ToolCategory.API,
        ideal_use_cases=[UseCase.RESEARCH, UseCase.DATA],
        overlap_tools=["openai_api", "anthropic_api"],
        pricing_type=PricingType.USAGE,
        enterprise_threshold=None,
        token_intensity=1.5,
        strengths=[
            "Very competitive pricing (flash-lite at $0.02/1M input)",
            "Native multimodal support",
            "Long context windows (1M+ tokens)",
        ],
        weaknesses=[
            "Fewer third-party library integrations",
            "Less mature developer ecosystem vs OpenAI",
        ],
    ),
}
