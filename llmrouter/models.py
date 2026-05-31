from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ModelConfig:
    """
    Configuration for a single LLM model.

    Attributes:
        model_id:       Full model identifier (e.g. 'groq/llama-3.1-8b-instant')
        provider:       Provider name: 'groq' | 'openai' | 'anthropic'
        name:           Short model name (e.g. 'llama-3.1-8b-instant')
        cost_per_1k:    Cost in USD per 1,000 tokens (input+output average)
        context_window: Max context length in tokens
        speed:          Relative speed: 'fast' | 'medium' | 'slow'
        quality:        Relative quality: 1 (lowest) – 10 (highest)
        api_key:        API key (overrides env var if set)
    """
    model_id: str
    provider: str
    name: str
    cost_per_1k: float
    context_window: int
    speed: str = "medium"       # 'fast' | 'medium' | 'slow'
    quality: int = 5            # 1–10
    api_key: Optional[str] = None

    def can_handle(self, prompt_tokens: int) -> bool:
        return prompt_tokens <= self.context_window * 0.8  # 80% safety margin


# ── Built-in model presets ─────────────────────────────────────────────────────

PRESET_MODELS: dict[str, ModelConfig] = {
    # Groq
    "groq/llama-3.1-8b-instant": ModelConfig(
        model_id="groq/llama-3.1-8b-instant",
        provider="groq", name="llama-3.1-8b-instant",
        cost_per_1k=0.00005, context_window=8192,
        speed="fast", quality=4,
    ),
    "groq/llama-3.3-70b-versatile": ModelConfig(
        model_id="groq/llama-3.3-70b-versatile",
        provider="groq", name="llama-3.3-70b-versatile",
        cost_per_1k=0.00059, context_window=32768,
        speed="medium", quality=8,
    ),
    "groq/mixtral-8x7b-32768": ModelConfig(
        model_id="groq/mixtral-8x7b-32768",
        provider="groq", name="mixtral-8x7b-32768",
        cost_per_1k=0.00024, context_window=32768,
        speed="medium", quality=7,
    ),
    # OpenAI
    "openai/gpt-4o-mini": ModelConfig(
        model_id="openai/gpt-4o-mini",
        provider="openai", name="gpt-4o-mini",
        cost_per_1k=0.00015, context_window=128000,
        speed="fast", quality=6,
    ),
    "openai/gpt-4o": ModelConfig(
        model_id="openai/gpt-4o",
        provider="openai", name="gpt-4o",
        cost_per_1k=0.005, context_window=128000,
        speed="medium", quality=9,
    ),
    # Anthropic
    "anthropic/claude-haiku-3": ModelConfig(
        model_id="anthropic/claude-haiku-3",
        provider="anthropic", name="claude-3-haiku-20240307",
        cost_per_1k=0.00025, context_window=200000,
        speed="fast", quality=6,
    ),
    "anthropic/claude-sonnet-4": ModelConfig(
        model_id="anthropic/claude-sonnet-4",
        provider="anthropic", name="claude-sonnet-4-5",
        cost_per_1k=0.003, context_window=200000,
        speed="medium", quality=9,
    ),
}
