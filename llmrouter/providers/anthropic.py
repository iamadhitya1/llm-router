import os
from typing import Optional
from .base import BaseProvider


class AnthropicProvider(BaseProvider):
    def complete(self, prompt, model_name, system, temperature, max_tokens, api_key):
        try:
            import anthropic
        except ImportError:
            raise ImportError("Install anthropic: pip install anthropic")

        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError("ANTHROPIC_API_KEY not set.")

        client = anthropic.Anthropic(api_key=key)
        kwargs = dict(
            model=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        if system:
            kwargs["system"] = system

        res = client.messages.create(**kwargs)
        return res.content[0].text.strip()
