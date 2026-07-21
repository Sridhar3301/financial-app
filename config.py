"""
Central configuration for the multi-agent financial advisor system.
Loads settings from environment variables / .env file.
"""

import os
from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised when required configuration is missing or invalid."""
    pass


load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic").lower().strip()

# -------------------------------
# Anthropic
# -------------------------------

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5")

# -------------------------------
# Gemini
# -------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# -------------------------------
# Groq
# -------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# -------------------------------

ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "false").lower() == "true"
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

# -------------------------------
# Provider validation
# -------------------------------

if LLM_PROVIDER not in ("anthropic", "gemini", "groq"):
    raise ConfigError(
        "LLM_PROVIDER must be 'anthropic', 'gemini', or 'groq'."
    )

if LLM_PROVIDER == "anthropic" and not ANTHROPIC_API_KEY:
    raise ConfigError(
        "ANTHROPIC_API_KEY is not set."
    )

if LLM_PROVIDER == "gemini" and not GEMINI_API_KEY:
    raise ConfigError(
        "GEMINI_API_KEY is not set."
    )

if LLM_PROVIDER == "groq" and not GROQ_API_KEY:
    raise ConfigError(
        "GROQ_API_KEY is not set."
    )