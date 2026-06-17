from setuptools import setup, find_packages

setup(
    name="llm-dispatch",
    version="1.0.1",
    author="M. Adhitya",
    author_email="adhitya5119@gmail.com",
    description="Route prompts to the right LLM by complexity. Supports Groq, OpenAI, Anthropic. Save cost, keep quality.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iamadhitya1/llm-router",
    project_urls={
        "Homepage": "https://iamadhitya.vercel.app",
        "Source": "https://github.com/iamadhitya1/llm-router",
        "Rewrite Labs": "https://rewritelabs.vercel.app",
    },
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "groq": ["groq>=0.4.0"],
        "openai": ["openai>=1.0.0"],
        "anthropic": ["anthropic>=0.20.0"],
        "all": ["groq>=0.4.0", "openai>=1.0.0", "anthropic>=0.20.0"],
    },
    python_requires=">=3.9",
    license="MIT",
    keywords=["llm", "router", "groq", "openai", "anthropic", "ai", "prompt-routing",
              "llm-routing", "model-routing", "cost-optimization", "ai-gateway",
              "multi-llm", "llm-proxy", "complexity-routing", "llm-dispatch"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
