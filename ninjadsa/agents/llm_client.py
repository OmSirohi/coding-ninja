import os
from typing import Optional

# Official Gemini SDK
from google import genai
from google.genai import types

class LLMClient:
    """
    Gemini client for optional refinement. If GEMINI_API_KEY is not set,
    this falls back to returning the original text (offline-safe).
    """
    def __init__(self):
        # default to Gemini Flash; change via LLM_MODEL in .env if you want
        self.model = os.environ.get("LLM_MODEL", "gemini-1.5-flash")
        self._enabled = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
        self._client = genai.Client() if self._enabled else None

    def refine(self, text: str, system_hint: Optional[str] = None, max_output_tokens: int = 512) -> str:
        """Return a polished version of `text` using Gemini. Offline-safe: returns original on any issue."""
        if not self._enabled:
            return text  # offline fallback

        prompt = text if not system_hint else f"{system_hint}\n\n{text}"
        try:
            resp = self._client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_output_tokens,
                    # For gemini-2.5-flash you can also set a thinking budget to 0 to reduce latency/cost:
                    # thinking_config=types.ThinkingConfig(thinking_budget=0),
                ),
            )
            return (resp.text or text).strip()
        except Exception:
            return text
