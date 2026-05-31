import os
from typing import Optional
from .base import BaseProvider


class GroqProvider(BaseProvider):
    def complete(self, prompt, model_name, system, temperature, max_tokens, api_key):
        try:
            from groq import Groq
        except ImportError:
            raise ImportError("Install groq: pip install groq")

        key = api_key or os.environ.get("GROQ_API_KEY")
        if not key:
            raise ValueError("GROQ_API_KEY not set.")

        client = Groq(api_key=key)
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        res = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return res.choices[0].message.content.strip()
