"""Structural validation shared by HTTP manifests and the adapter."""
from __future__ import annotations

import ipaddress
from urllib.parse import urlsplit


def endpoint_origin(url: str) -> tuple[str, str, int | None]:
    if not isinstance(url, str):
        raise ValueError("Agent endpoint must be a valid HTTPS URL")
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except (TypeError, ValueError) as exc:
        raise ValueError("Agent endpoint must be a valid HTTPS URL") from exc
    if (parsed.scheme not in {"https", "http"} or not parsed.hostname
            or parsed.username is not None or parsed.password is not None):
        raise ValueError("Agent endpoint must be an HTTPS URL without embedded credentials")
    if parsed.query or parsed.fragment:
        raise ValueError("Agent endpoint must not contain a query or fragment")
    host = parsed.hostname.lower()
    if parsed.scheme == "http":
        try:
            loopback = ipaddress.ip_address(host).is_loopback
        except ValueError:
            loopback = host == "localhost"
        if not loopback:
            raise ValueError("Plain HTTP is allowed only for localhost")
    return parsed.scheme, host, port
