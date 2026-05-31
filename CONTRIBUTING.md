# Contributing to llm-router (llm-dispatch)

PRs welcome. Here's how to get started.

## Setup

```bash
git clone https://github.com/iamadhitya1/llm-router
cd llm-router
pip install -e ".[all]"
```

## Project structure

```
llmrouter/
  __init__.py    # exports LLMRouter, ModelConfig, complexity_score
  router.py      # main LLMRouter class
  scorer.py      # complexity_score() function
  models.py      # PRESET_MODELS, ModelConfig
  providers/     # Groq, OpenAI, Anthropic adapters
```

## What's in scope

- Bug fixes
- New provider adapters (Cohere, Mistral, Together AI, etc.)
- Improvements to `complexity_score()` accuracy
- New routing strategies beyond `auto/cheapest/fastest/smartest/balanced`
- Streaming response support
- Documentation fixes

## Guidelines

- Keep `LLMRouter` as the primary public API
- New providers go in `providers/` as a new file — don't modify existing adapters
- The `complexity_score()` function must stay fast (no API calls, pure computation)
- Don't break existing `.add()` / `.complete()` signatures
- One feature or fix per PR

## Submitting a PR

1. Fork the repo
2. Create a branch: `git checkout -b feat/your-feature-name`
3. Make your change
4. Open a PR against `main` with a clear title and description of what changed and why

Set provider API keys in your environment to test against real models.

---

MIT © 2025 M Adhitya · [Rewrite Labs](https://rewritelabs.vercel.app)
