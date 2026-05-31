"""
LLMRouter — routes prompts to the right model based on complexity,
cost, speed, or quality preference.
"""

from dataclasses import dataclass
from typing import Optional
from .models import ModelConfig, PRESET_MODELS
from .scorer import complexity_score, estimate_tokens
from .providers import PROVIDERS


@dataclass
class RouteResult:
    """Result of a routed LLM call."""
    output: str
    model_used: str
    provider: str
    complexity_score: float
    strategy: str
    estimated_cost_usd: float

    def __repr__(self):
        return (
            f"RouteResult(model='{self.model_used}', "
            f"strategy='{self.strategy}', "
            f"complexity={self.complexity_score:.2f}, "
            f"cost=${self.estimated_cost_usd:.6f})"
        )


class LLMRouter:
    """
    Routes prompts to the best LLM based on your strategy.

    Strategies:
        'auto'     — analyses complexity, balances cost vs quality (default)
        'cheapest' — always picks lowest cost model that fits context
        'fastest'  — always picks fastest model
        'smartest' — always picks highest quality model
        'balanced' — balances speed and quality equally

    Usage:
        router = LLMRouter()
        router.add("groq/llama-3.1-8b-instant")
        router.add("groq/llama-3.3-70b-versatile")
        router.add("openai/gpt-4o")

        result = router.complete("What is 2+2?")
        print(result.output)      # 4
        print(result.model_used)  # llama-3.1-8b-instant (cheap, fast)

        result = router.complete("Refactor this 200-line Python class...")
        print(result.model_used)  # gpt-4o (complex task)
    """

    def __init__(
        self,
        strategy: str = "auto",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        system: Optional[str] = None,
        verbose: bool = False,
    ):
        """
        Args:
            strategy:    Routing strategy (default: 'auto')
            temperature: Sampling temperature (default: 0.7)
            max_tokens:  Max output tokens (default: 1024)
            system:      System prompt applied to all calls
            verbose:     Print routing decisions (default: False)
        """
        self._models: list[ModelConfig] = []
        self._strategy = strategy
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._system = system
        self._verbose = verbose

    # ── Model Registry ─────────────────────────────────────────────────────────

    def add(self, model_id: str, api_key: Optional[str] = None) -> "LLMRouter":
        """
        Add a model to the router by preset ID.

        Args:
            model_id: e.g. 'groq/llama-3.3-70b-versatile', 'openai/gpt-4o'
            api_key:  Optional API key override for this model.
        """
        if model_id not in PRESET_MODELS:
            raise ValueError(
                f"Unknown model '{model_id}'. "
                f"Available: {list(PRESET_MODELS.keys())}"
            )
        config = PRESET_MODELS[model_id]
        if api_key:
            config.api_key = api_key
        self._models.append(config)
        return self

    def add_custom(self, config: ModelConfig) -> "LLMRouter":
        """Add a custom model configuration."""
        self._models.append(config)
        return self

    # ── Routing ────────────────────────────────────────────────────────────────

    def complete(
        self,
        prompt: str,
        strategy: Optional[str] = None,
        system: Optional[str] = None,
    ) -> RouteResult:
        """
        Route the prompt to the best model and return the result.

        Args:
            prompt:   The user prompt.
            strategy: Override the default strategy for this call.
            system:   Override system prompt for this call.

        Returns:
            RouteResult with output, model_used, cost, complexity_score.
        """
        if not self._models:
            raise RuntimeError("No models added. Call .add('model_id') first.")

        strat = strategy or self._strategy
        score = complexity_score(prompt)
        tokens = estimate_tokens(prompt)

        candidates = [m for m in self._models if m.can_handle(tokens)]
        if not candidates:
            candidates = sorted(self._models, key=lambda m: m.context_window, reverse=True)[:1]

        selected = self._select(candidates, score, strat)

        if self._verbose:
            print(
                f"[llm-router] strategy={strat} | complexity={score:.2f} | "
                f"tokens≈{tokens} | → {selected.model_id}"
            )

        provider = PROVIDERS.get(selected.provider)
        if not provider:
            raise ValueError(f"Unsupported provider '{selected.provider}'")

        output = provider.complete(
            prompt=prompt,
            model_name=selected.name,
            system=system or self._system,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            api_key=selected.api_key,
        )

        estimated_cost = (tokens / 1000) * selected.cost_per_1k

        return RouteResult(
            output=output,
            model_used=selected.name,
            provider=selected.provider,
            complexity_score=score,
            strategy=strat,
            estimated_cost_usd=round(estimated_cost, 8),
        )

    def models(self) -> list[dict]:
        """List all registered models."""
        return [
            {
                "model_id": m.model_id,
                "provider": m.provider,
                "cost_per_1k": m.cost_per_1k,
                "speed": m.speed,
                "quality": m.quality,
                "context_window": m.context_window,
            }
            for m in self._models
        ]

    # ── Selection Logic ────────────────────────────────────────────────────────

    def _select(self, candidates: list[ModelConfig], score: float, strategy: str) -> ModelConfig:
        if strategy == "cheapest":
            return min(candidates, key=lambda m: m.cost_per_1k)

        if strategy == "fastest":
            order = {"fast": 0, "medium": 1, "slow": 2}
            return min(candidates, key=lambda m: order.get(m.speed, 1))

        if strategy == "smartest":
            return max(candidates, key=lambda m: m.quality)

        if strategy == "balanced":
            speed_order = {"fast": 3, "medium": 2, "slow": 1}
            return max(candidates, key=lambda m: m.quality + speed_order.get(m.speed, 2))

        # auto — complexity-aware routing
        if score < 0.25:
            # Simple prompt → cheapest fast model
            fast = [m for m in candidates if m.speed == "fast"]
            pool = fast if fast else candidates
            return min(pool, key=lambda m: m.cost_per_1k)
        elif score < 0.6:
            # Medium complexity → balance cost and quality
            return max(candidates, key=lambda m: m.quality / (m.cost_per_1k + 0.001))
        else:
            # Complex prompt → highest quality
            return max(candidates, key=lambda m: m.quality)
