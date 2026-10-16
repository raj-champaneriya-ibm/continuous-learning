"""Who writes the draft in step 5.

* ClaudeCodeProvider — calls `claude -p` (Claude Code headless mode) with your Claude Code login.
* OfflineProvider    — a rule-based stand-in so you can try the app with no model. It has deliberate
                       flaws (promises fix times, offers 50% to everyone) so the checks have work to do.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from .lab import INTENTS

DRAFT_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string", "enum": INTENTS},
        "reply": {"type": "string"},
        "needs_human": {"type": "boolean"},
        "escalation_reason": {"type": "string"},
        "cited_sources": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["intent", "reply", "needs_human", "escalation_reason", "cited_sources"],
}

# Built-in tools the drafter never needs. The temp working directory is empty anyway.
BLOCKED_TOOLS = "Bash,Edit,Write,NotebookEdit,WebFetch,WebSearch,Agent,Task,mcp__*"


def _result(output=None, error=None, latency=0.0, cost=None, raw=""):
    return {"output": output, "error": error, "latency_s": round(latency, 2), "cost_usd": cost, "raw": raw}


def _parse_json_text(text: str):
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    start, end = text.find("{"), text.rfind("}")
    return json.loads(text[start:end + 1]) if start >= 0 and end > start else None


class ClaudeCodeProvider:
    name = "claude-code"
    label = "Claude Code"

    def __init__(self, model: str = "sonnet", timeout: int = 180, binary: str | None = None):
        self.model, self.timeout = model, timeout
        self.binary = binary or shutil.which("claude")

    def status(self) -> tuple[bool, str]:
        if not self.binary:
            return False, "The `claude` command isn't on PATH. Install Claude Code, then run `claude` once to log in."
        try:
            out = subprocess.run([self.binary, "auth", "status"], capture_output=True, text=True, timeout=20)
            info = json.loads(out.stdout or "{}")
            if info.get("loggedIn"):
                return True, f"Logged in ({info.get('authMethod')}). Model: {self.model}."
            return False, "Claude Code is installed but not logged in. Run `claude` in a terminal and log in."
        except Exception as exc:  # noqa: BLE001 - surface anything to the UI
            return False, f"Couldn't check Claude Code login: {exc}"

    @property
    def schema_flag_ok(self) -> bool:
        # npm's claude.cmd on Windows goes through cmd.exe, which mangles inline JSON arguments.
        # There we ask for JSON in the prompt instead and parse the text result.
        return not str(self.binary).lower().endswith((".cmd", ".bat"))

    def command(self, system_prompt_file: str) -> list[str]:
        schema = ["--json-schema", json.dumps(DRAFT_SCHEMA)] if self.schema_flag_ok else []
        return [self.binary, "-p",
                "--output-format", "json", *schema,
                "--system-prompt-file", system_prompt_file,   # replaces Claude Code's coding prompt
                "--model", self.model,
                "--disallowedTools", BLOCKED_TOOLS,
                "--strict-mcp-config",                          # no MCP servers
                "--setting-sources", "user",                    # ignore project settings
                "--permission-mode", "dontAsk",
                "--no-session-persistence"]

    def draft(self, system: str, user: str, ctx: dict | None = None) -> dict:
        if not self.binary:
            return _result(error="Claude Code (`claude`) not found on PATH.")
        started = time.time()
        with tempfile.TemporaryDirectory(prefix="acme-draft-") as tmp:
            prompt_file = Path(tmp) / "system.md"
            if not self.schema_flag_ok:
                system += ("\n\nAnswer with ONLY a JSON object matching this schema, no other text:\n"
                           + json.dumps(DRAFT_SCHEMA))
            prompt_file.write_text(system, encoding="utf-8")
            try:
                proc = subprocess.run(self.command(str(prompt_file)), input=user, capture_output=True,
                                      text=True, encoding="utf-8", timeout=self.timeout, cwd=tmp)
            except subprocess.TimeoutExpired:
                return _result(error=f"Claude Code timed out after {self.timeout}s.", latency=time.time() - started)
        latency = time.time() - started
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError:
            return _result(error=(proc.stderr or proc.stdout or "No output").strip()[:400], latency=latency,
                           raw=proc.stdout)
        if data.get("is_error") or data.get("subtype") not in (None, "success"):
            return _result(error=str(data.get("result") or data.get("subtype"))[:400], latency=latency,
                           cost=data.get("total_cost_usd"), raw=proc.stdout)
        output = data.get("structured_output")
        if output is None:
            try:
                output = _parse_json_text(data.get("result", ""))
            except json.JSONDecodeError:
                output = None
        if not output:
            return _result(error="Claude Code returned no structured draft.", latency=latency,
                           cost=data.get("total_cost_usd"), raw=proc.stdout)
        return _result(output=output, latency=latency, cost=data.get("total_cost_usd"), raw=proc.stdout)


class OfflineProvider:
    name = "offline"
    label = "Offline stand-in (no model)"
    model = "rules"

    def status(self) -> tuple[bool, str]:
        return True, "Rule-based drafts so you can try the app. Not a model, and wrong on purpose sometimes."

    KEYWORDS = {
        "outage": ["down", "no internet", "not working", "net band", "dead", "stopped working"],
        "billing": ["bill", "charge", "refund", "payment", "paid", "fee", "autopay"],
        "speed": ["slow", "speed", "buffer", "lag", "mbps", "ping"],
        "cancel": ["cancel", "close the connection", "band karna"],
        "upgrade": ["upgrade", "downgrade", "gbps", "pro plan", "plan with", "faster"],
        "relocation": ["shift", "moving", "move my", "relocat", "transfer the account"],
    }

    def draft(self, system: str, user: str, ctx: dict | None = None) -> dict:
        ctx = ctx or {}
        msg = (ctx.get("message") or "").lower()
        customer, outage = ctx.get("customer") or {}, ctx.get("outage")
        first = (customer.get("name") or "there").split()[0]
        scores = {k: sum(w in msg for w in ws) for k, ws in self.KEYWORDS.items()}
        intent = max(scores, key=scores.get) if max(scores.values()) else "other"

        body = {
            "outage": (f"There is a known outage in {customer.get('area')} (ticket {outage['ticket']}): "
                       f"{outage['cause'].lower()}. {outage['status']}"
                       + (" Our engineers expect to have it fixed by this evening." if re.search(r"when|kab", msg) else "")
                       ) if outage else ("There's no known outage in your area. Please restart your router "
                                         "(switch it off for 30 seconds); if it still doesn't work we'll book a "
                                         "technician visit."),
            "billing": "Bills are due by the 10th, and a ₹100 late fee is added to bills paid after that.",
            "speed": ("Please restart the router (switch it off for 30 seconds), then test the speed on a cable "
                      "connection at fast.com. If it's below half your plan speed, we'll book a free technician "
                      "visit within 2 working days."),
            "cancel": ("Cancellation needs 30 days of notice and we collect the router free of charge. "
                       "If you'd like to stay, we can offer 50% off for 1 month."),
            "upgrade": ("Our plans are Basic 100 Mbps (₹699), Plus 300 Mbps (₹999) and Pro 1 Gbps (₹1,499) per "
                        "month. Upgrades are active within 1 hour."),
            "relocation": "Shifting is free within our Pune service areas, and re-installation happens within 48 hours.",
            "other": ("Acme staff never ask for OTPs or passwords. You can change your Wi-Fi password in the Acme "
                      "app under Wi-Fi settings."),
        }[intent]

        reasons = []
        if re.search(r"court|legal|lawyer|trai", msg):
            reasons.append("legal threat")
        if re.search(r"otp", msg) and re.search(r"called|asked|someone", msg):
            reasons.append("possible fraud")
        if re.search(r"refund|compensation|credit|money back", msg) and any(
                int(a.replace(",", "")) > 500 for a in re.findall(r"₹(\d[\d,]*)", msg)):
            reasons.append("refund above ₹500")
        reply = f"Hi {first},\n\n{body}\n\nAcme Fibre Support"
        cited = {"outage": ["OUTAGE", "KB05"], "billing": ["KB01", "KB02"], "speed": ["KB07", "KB08"],
                 "cancel": ["KB10", "KB11"], "upgrade": ["KB09"], "relocation": ["KB12"], "other": ["KB13", "KB15"]}
        time.sleep(0.15)
        return _result(output={"intent": intent, "reply": reply, "needs_human": bool(reasons),
                               "escalation_reason": ", ".join(reasons), "cited_sources": cited[intent] + ["CRM"]},
                       latency=0.15)


def make_provider(name: str, model: str = "sonnet"):
    return ClaudeCodeProvider(model=model) if name == "claude-code" else OfflineProvider()
