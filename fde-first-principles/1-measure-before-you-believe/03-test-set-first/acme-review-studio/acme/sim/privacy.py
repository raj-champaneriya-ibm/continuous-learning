"""Redact credentials and common customer secrets before persisting evidence."""
from __future__ import annotations

import os
import re
from typing import Any

from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

_SECRET_KEYS = frozenset({"authorization", "proxy-authorization", "x-api-key", "api_key", "apikey",
                          "password", "passwd", "secret", "access_token", "refresh_token", "token",
                          "otp", "one_time_password", "passcode", "pin", "cvv"})
_SECRET_TEXT = re.compile(
    r"(?i)(\b(?:otp|one[- ]time password|password|passcode|pin|cvv)\b"
    r"\s*(?:is|was|=|:)\s*)([^\s,;.!?]+)"
)
_SECRET_BARE = re.compile(r"(?i)(\b(?:otp|pin|cvv)\b\s+)(\d{4,8})\b")
_AUTH_TEXT = re.compile(r"(?i)(\b(?:authorization|x-api-key)\s*[:=]\s*)(?:bearer\s+)?[^\s,;]+")


def secret_values(*names: str) -> tuple[str, ...]:
    values = [os.environ[name] for name in names if os.environ.get(name)]
    try:
        from lab import llm
    except ModuleNotFoundError as exc:
        if exc.name != "lab":
            raise
    else:
        for name in names:
            if name.startswith("LLM_"):
                value = llm._env(name)
                if value:
                    values.append(value)
    return tuple(dict.fromkeys(values))


def redact(value: Any, *, secrets: tuple[str, ...] = ()) -> Any:
    if isinstance(value, dict):
        return {
            str(key): ("[REDACTED]" if str(key).lower() in _SECRET_KEYS
                       and not (isinstance(item, str) and item.startswith("env:"))
                       else redact(item, secrets=secrets))
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item, secrets=secrets) for item in value]
    if isinstance(value, tuple):
        return tuple(redact(item, secrets=secrets) for item in value)
    if isinstance(value, str):
        text = _SECRET_TEXT.sub(r"\1[REDACTED]", value)
        text = _SECRET_BARE.sub(r"\1[REDACTED]", text)
        text = _AUTH_TEXT.sub(r"\1[REDACTED]", text)
        for secret in secrets:
            if secret:
                text = text.replace(secret, "[REDACTED]")
        return text
    return value


class RedactingSerializer(JsonPlusSerializer):
    """Redact checkpoint contents before LangGraph writes them to SQLite."""

    def dumps_typed(self, obj: Any) -> tuple[str, bytes]:
        secrets = secret_values("LLM_API_KEY", "LLM_ANTHROPIC_KEY")
        return super().dumps_typed(redact(obj, secrets=secrets))
