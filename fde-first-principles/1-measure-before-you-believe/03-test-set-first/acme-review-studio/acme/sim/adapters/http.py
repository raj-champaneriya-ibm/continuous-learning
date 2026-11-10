"""Allowlisted HTTP adapter for an external draft agent."""
from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests

from ..trace import Capabilities, RunInput, RunResult, Span, Topology
from ..network import endpoint_origin
from ..versions import Version, VersionRegistry
from .common import direct_output
from .direct import DirectAdapter


def _endpoint(url: str) -> tuple[str, str, int | None]:
    scheme, host, port = endpoint_origin(url)
    allowed = {item.strip().lower() for item in os.environ.get("ACME_SIM_ALLOWED_HOSTS", "").split(",")
               if item.strip()}
    if host not in allowed:
        raise ValueError(f"Agent host {host!r} is not in ACME_SIM_ALLOWED_HOSTS")
    return scheme, host, port


class HttpAdapter(DirectAdapter):
    implementation = "api"

    def __init__(self, registry: VersionRegistry, checkpoints: Path, log_path: Path):
        super().__init__(registry, checkpoints, log_path)

    def capabilities(self, version: Version) -> Capabilities:
        return Capabilities(remote_trace=True)

    def status(self, version: Version) -> tuple[bool, str]:
        config = version.content["config"]
        try:
            _endpoint(config.get("endpoint") or "")
            auth = config.get("auth")
            if auth and not os.environ.get(auth.removeprefix("env:")):
                return False, f"Set {auth.removeprefix('env:')} before running this version."
            if config.get("output_schema", "draft-v1") != "draft-v1":
                return False, "Only the draft-v1 output schema is supported."
        except ValueError as exc:
            return False, str(exc)
        return True, "Endpoint is allowlisted."

    def topology(self, version: Version) -> Topology:
        return Topology(nodes=[{"id": "http", "name": "HTTP exchange"}], edges=[])

    def start(self, version: Version, run_input: RunInput, run_id: str, sample: int = 0,
              recorded: dict[str, Any] | None = None,
              cancelled: threading.Event | None = None) -> RunResult:
        if recorded is not None:
            raise ValueError("This adapter does not support recorded replay")
        ready, message = self.status(version)
        if not ready:
            raise ValueError(message)
        config = version.content["config"]
        url = config["endpoint"]
        origin = _endpoint(url)
        lab = self.registry.load_lab(version)
        if run_input.customer_id not in lab.customers:
            output = direct_output(lab, config, run_input, None, provider="http-json", model="")
            return RunResult(run_id=run_id, version_id=version.id, state="completed", output=output,
                             spans=[Span(id="verify", parent=None, kind="guard", name="Verify account",
                                         status="stop", ms=0, attrs={"reason": output["reasons"][0]})])
        payload = {key: getattr(run_input, key) for key in version.content["inputs"]}
        auth = config.get("auth")
        secret = os.environ.get(auth.removeprefix("env:"), "") if auth else ""
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if auth:
            headers["Authorization"] = f"Bearer {secret}"
        cap = config.get("max_response_bytes", 1_048_576)
        if isinstance(cap, bool) or not isinstance(cap, int) or not 1 <= cap <= 5_242_880:
            raise ValueError("max_response_bytes must be between 1 and 5242880")
        started = time.monotonic()
        session = requests.Session()
        session.trust_env = False
        try:
            for _ in range(4):
                remaining = config["timeout_s"] - (time.monotonic() - started)
                if remaining <= 0:
                    raise TimeoutError("HTTP agent exceeded its run timeout")
                response = session.post(url, json=payload, headers=headers, timeout=remaining,
                                        allow_redirects=False, stream=True)
                if response.status_code not in {301, 302, 303, 307, 308}:
                    break
                location = response.headers.get("Location")
                response.close()
                if not location:
                    raise ValueError("Agent redirect has no Location")
                target = urljoin(url, location)
                if _endpoint(target) != origin:
                    raise ValueError("Agent redirects must stay on the original allowlisted origin")
                url = target
            else:
                raise ValueError("Too many agent redirects")
            try:
                response.raise_for_status()
                body = bytearray()
                for chunk in response.iter_content(chunk_size=65536):
                    if (cancelled and cancelled.is_set()) or time.monotonic() - started > config["timeout_s"]:
                        raise TimeoutError("HTTP agent exceeded its run timeout")
                    body.extend(chunk)
                    if len(body) > cap:
                        raise ValueError("Agent response exceeded the size limit")
                data = json.loads(body)
            finally:
                response.close()
        finally:
            session.close()
        if not isinstance(data, dict):
            raise ValueError("Agent response must be a JSON object")
        draft = data.get("output", data)
        output = direct_output(lab, config, run_input, draft, provider="http-json", model=config.get("model", ""))
        elapsed = time.monotonic() - started
        spans = [Span(id="http", parent=None, kind="http", name="HTTP exchange", status="ok", ms=int(elapsed * 1000),
                      attrs={"method": "POST", "url": url, "status_code": response.status_code,
                             "request": payload, "response": data, "headers": {"authorization": "[REDACTED]"},
                             "bytes": len(body)})]
        remote = data.get("spans") or []
        if not isinstance(remote, list) or len(remote) > 256:
            raise ValueError("Remote spans must be a list of at most 256 entries")
        seen = set()
        for item in remote:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str) or item["id"] in seen:
                raise ValueError("Remote spans need unique string ids")
            seen.add(item["id"])
        for item in remote:
            parent = item.get("parent")
            if parent is not None and (parent not in seen or parent == item["id"]):
                raise ValueError("Remote span has an invalid parent")
            spans.append(Span(id=f"remote:{item['id']}", parent=f"remote:{parent}" if parent else "http",
                              kind=item["kind"], name=str(item["name"]), status=item["status"],
                              ms=int(item.get("ms", 0)), attrs=item.get("attrs") or {}))
        return RunResult(run_id=run_id, version_id=version.id, state="completed", output=output, spans=spans,
                         usage={"latency_s": round(elapsed, 3), "cost_usd": data.get("cost_usd"),
                                "tokens_in": data.get("tokens_in"), "tokens_out": data.get("tokens_out")})
