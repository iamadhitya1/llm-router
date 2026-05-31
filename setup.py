from setuptools import setup, find_packages

setup(
    name="llm-dispatch",
    version="1.0.0",
    author="M Adhitya",
    description="Route prompts to the right LLM automatically. Supports Groq, OpenAI, Anthropic.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iamadhitya1/llm-router",
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
    keywords=["llm", "router", "groq", "openai", "anthropic", "ai", "prompt-routing"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
