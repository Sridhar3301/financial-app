"""
BaseAgent: shared logic for calling an LLM (Claude, Gemini, or Groq)
and robustly parsing a JSON object out of the response.
"""

import json
import re

from config import (
    LLM_PROVIDER,
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    MAX_TOKENS,
)

# Lazy clients
_anthropic_client = None
_gemini_client = None
_groq_client = None


def _get_anthropic_client():
    global _anthropic_client
    if _anthropic_client is None:
        from anthropic import Anthropic
        _anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
    return _anthropic_client


def _get_gemini_client():
    global _gemini_client
    if _gemini_client is None:
        from google import genai
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    return _gemini_client


def _get_groq_client():
    global _groq_client
    if _groq_client is None:
        from openai import OpenAI

        _groq_client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

    return _groq_client


class AgentError(Exception):
    pass


class BaseAgent:
    """Base class for all pipeline agents."""

    name = "BaseAgent"
    system_prompt = ""

    def __init__(self, use_web_search: bool = False, model: str = None):
        self.use_web_search = use_web_search
        self.provider = LLM_PROVIDER

        if model:
            self.model = model
        else:
            if self.provider == "anthropic":
                self.model = CLAUDE_MODEL
            elif self.provider == "gemini":
                self.model = GEMINI_MODEL
            elif self.provider == "groq":
                self.model = GROQ_MODEL
            else:
                raise AgentError(f"Unsupported provider: {self.provider}")

    # -----------------------------------------------------------------
    # Claude
    # -----------------------------------------------------------------

    def _call_claude(self, user_message: str) -> str:
        client = _get_anthropic_client()

        kwargs = dict(
            model=self.model,
            max_tokens=MAX_TOKENS,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
        )

        if self.use_web_search:
            kwargs["tools"] = [
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                }
            ]

        response = client.messages.create(**kwargs)

        text_parts = [
            block.text
            for block in response.content
            if block.type == "text"
        ]

        return "\n".join(text_parts).strip()

    # -----------------------------------------------------------------
    # Gemini
    # -----------------------------------------------------------------

    def _call_gemini(self, user_message: str) -> str:
        from google.genai import types

        client = _get_gemini_client()

        tools = None
        if self.use_web_search:
            tools = [
                types.Tool(
                    google_search=types.GoogleSearch()
                )
            ]

        config = types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            max_output_tokens=MAX_TOKENS,
            tools=tools,
        )

        response = client.models.generate_content(
            model=self.model,
            contents=user_message,
            config=config,
        )

        return (response.text or "").strip()

    # -----------------------------------------------------------------
    # Groq
    # -----------------------------------------------------------------

    def _call_groq(self, user_message: str) -> str:

        client = _get_groq_client()

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            temperature=0.2,
            max_tokens=MAX_TOKENS,
            response_format={"type": "json_object"},
        )

        return response.choices[0].message.content.strip()

    # -----------------------------------------------------------------
    # Provider Router
    # -----------------------------------------------------------------

    def _call_llm(self, user_message: str) -> str:

        if self.provider == "anthropic":
            return self._call_claude(user_message)

        elif self.provider == "gemini":
            return self._call_gemini(user_message)

        elif self.provider == "groq":
            return self._call_groq(user_message)

        raise AgentError(f"Unsupported provider: {self.provider}")

    # -----------------------------------------------------------------
    # JSON handling
    # -----------------------------------------------------------------

    @staticmethod
    def _extract_json(raw_text: str) -> dict:
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        match = re.search(r"\{.*\}", cleaned, re.DOTALL)

        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError as e:
                raise AgentError(
                    f"Could not parse JSON from model output: {e}\n\n{raw_text}"
                )

        raise AgentError(
            f"Could not find JSON object in model output.\n\n{raw_text}"
        )

    # -----------------------------------------------------------------

    def run(self, user_message: str) -> dict:
        raw = self._call_llm(user_message)
        return self._extract_json(raw)