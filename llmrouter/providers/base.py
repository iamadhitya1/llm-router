from abc import ABC, abstractmethod
from typing import Optional


class BaseProvider(ABC):
    """Base class for all LLM providers."""

    @abstractmethod
    def complete(
        self,
        prompt: str,
        model_name: str,
        system: Optional[str],
        temperature: float,
        max_tokens: int,
        api_key: Optional[str],
    ) -> str:
        pass
