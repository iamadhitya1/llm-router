"""
Prompt complexity scorer — estimates how 'hard' a prompt is
so the router can pick an appropriately powerful model.
"""

import re


# Keywords that signal complex reasoning tasks
COMPLEX_KEYWORDS = [
    "analyze", "analyse", "explain", "compare", "evaluate", "critique",
    "summarize", "summarise", "translate", "refactor", "debug", "review",
    "write", "generate", "create", "design", "plan", "strategy",
    "legal", "medical", "financial", "technical", "research",
    "step by step", "in detail", "comprehensive", "thorough",
    "code", "function", "algorithm", "architecture", "implement",
]

SIMPLE_KEYWORDS = [
    "what is", "who is", "when", "where", "define",
    "how many", "how much", "list", "name", "give me",
    "yes or no", "true or false",
]


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return max(1, len(text) // 4)


def complexity_score(prompt: str) -> float:
    """
    Score prompt complexity from 0.0 (trivial) to 1.0 (very complex).

    Factors:
    - Prompt length
    - Presence of complex/simple keywords
    - Number of questions asked
    - Code blocks or technical content
    - Multi-part instructions
    """
    score = 0.0
    lower = prompt.lower()
    tokens = estimate_tokens(prompt)

    # Length factor (0–0.3)
    if tokens < 50:
        score += 0.0
    elif tokens < 200:
        score += 0.1
    elif tokens < 500:
        score += 0.2
    else:
        score += 0.3

    # Complex keywords (0–0.25)
    matches = sum(1 for kw in COMPLEX_KEYWORDS if kw in lower)
    score += min(matches * 0.05, 0.25)

    # Simple keywords reduce score (0–0.15)
    simple_matches = sum(1 for kw in SIMPLE_KEYWORDS if kw in lower)
    score -= min(simple_matches * 0.05, 0.15)

    # Code blocks (0–0.2)
    if "```" in prompt or "def " in prompt or "function " in prompt:
        score += 0.2

    # Multiple questions (0–0.15)
    question_count = prompt.count("?")
    score += min(question_count * 0.05, 0.15)

    # Multi-part instructions
    if re.search(r'\b(and|also|additionally|furthermore|then)\b', lower):
        score += 0.05

    return round(max(0.0, min(1.0, score)), 3)
