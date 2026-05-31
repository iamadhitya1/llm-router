from .groq import GroqProvider
from .openai import OpenAIProvider
from .anthropic import AnthropicProvider

PROVIDERS = {
    "groq": GroqProvider(),
    "openai": OpenAIProvider(),
    "anthropic": AnthropicProvider(),
}
