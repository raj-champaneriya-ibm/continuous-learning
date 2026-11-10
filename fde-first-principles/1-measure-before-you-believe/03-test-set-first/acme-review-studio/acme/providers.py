"""Who writes the draft in step 5.

* ClaudeCodeProvider — calls `claude -p` (Claude Code headless mode) with your Claude Code login.
* OfflineProvider    — a rule-based stand-in so you can try the app with no model. It has deliberate
                       flaws (promises fix times, offers 50% to everyone) so the checks have work to do.
* C3Provider         — the lab's ontology-grounded agent (fde-first-principles/lab/version_c3.py), so the
                       expert reviews the drafts of the agent the lab measures.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
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


# fde-first-principles/, the folder that holds the lab package (lab/version_c3.py).
LAB_ROOT = Path(__file__).resolve().parents[4]
C3_DEFAULT_MODEL = "anthropic:glm-5.3-flash"


def c3_output(row: dict, outage: dict | None = None) -> dict:
    """Map one lab version_c3 result row onto the draft the workflow expects (DRAFT_SCHEMA).

    escalation_reason lists C3's escalation_sources ("rule:money_above_headroom", "guard:reveals_limit",
    "model", ...), so the reviewer sees why C3 handed the email to a person. cited_sources comes from the
    tools C3 called: CRM for the customer lookup, KB ids for the help articles it read, OUTAGE when the
    reply names the area's outage ticket."""
    cited = []
    for call in row.get("tool_calls") or []:
        name, result = call.get("name"), call.get("result")
        if name == "lookup_customer":
            cited.append("CRM")
        elif name == "search_kb" and isinstance(result, list):
            cited += [r.get("id") for r in result if isinstance(r, dict)]
        elif name == "get_article" and isinstance(result, dict):
            cited.append(result.get("id"))
        elif name == "define_term" and isinstance(result, dict):
            cited += result.get("kb_articles") or []
    reply = row.get("reply") or ""
    if outage and outage.get("ticket") and outage["ticket"] in reply:
        cited.append("OUTAGE")
    intent = row.get("intent") if row.get("intent") in INTENTS else "other"
    return {"intent": intent, "reply": reply, "needs_human": bool(row.get("needs_human")),
            "escalation_reason": ", ".join(row.get("escalation_sources") or []),
            "cited_sources": list(dict.fromkeys(c for c in cited if c))}


class C3Provider:
    """The lab's ontology-grounded agent (fde-first-principles/lab/version_c3.py) writes the draft.

    C3 builds its own decision envelope from the case (entitlements, concepts, escalation triggers, offer
    decisions, the outage gate) and calls its own tools, so it ignores the prompts step 4 builds. It reads
    customers, policy, help articles and the ontology from fde-first-principles/data/acme, not from the
    workbook: edits made in the studio's Data tab don't reach it. The model comes from ACME_C3_MODEL
    (default anthropic:glm-5.3-flash) and its key from fde-first-principles/.env; the studio's Claude model
    setting doesn't apply. Answers are cached by the lab, so drafting the same email again is free."""
    name = "c3"
    label = "C3 ontology agent"

    def __init__(self, model: str | None = None, lab_root: Path | None = None, runner=None,
                 data_root: Path | None = None, temperature: float = 0.0, max_steps: int = 6,
                 timeout: float = 180, persist_cache: bool = True):
        self.model = model or os.environ.get("ACME_C3_MODEL") or C3_DEFAULT_MODEL
        self.lab_root = Path(lab_root or os.environ.get("ACME_LAB_ROOT") or LAB_ROOT)
        self.data_root = Path(data_root) if data_root else None
        self.temperature, self.max_steps = temperature, max_steps
        self.timeout = timeout
        self.persist_cache = persist_cache
        self._runner = runner
        self._native = runner is None
        self._llm = None

    def _load(self):
        if self._runner is None:
            if str(self.lab_root) not in sys.path:
                sys.path.append(str(self.lab_root))   # appended: the studio's own modules win any name clash
            from lab import llm
            from lab.version_c3 import run_agent
            self._llm, self._runner = llm, run_agent
        return self._runner

    def status(self) -> tuple[bool, str]:
        try:
            self._load()
        except ModuleNotFoundError as exc:
            if exc.name == "lab":
                return False, f"No lab package in {self.lab_root}. Set ACME_LAB_ROOT to your fde-first-principles folder."
            return False, f"The C3 agent needs {exc.name}: pip install -r requirements.txt"
        except Exception as exc:  # noqa: BLE001 - surface anything to the UI
            return False, (f"Couldn't load the lab from {self.lab_root}: {exc}. "
                           "Install the C3 packages: pip install -r requirements.txt")
        if self._llm is not None and self.model.startswith("anthropic:") and not (
                self._llm._env("LLM_ANTHROPIC_KEY") or self._llm._env("LLM_API_KEY")):
            return False, "Set LLM_ANTHROPIC_KEY in fde-first-principles/.env for the C3 model."
        return True, f"Lab agent from {self.lab_root.name}/lab. Model: {self.model}."

    def draft(self, system: str, user: str, ctx: dict | None = None) -> dict:
        ctx = ctx or {}
        customer = ctx.get("customer") or {}
        case = {"id": ctx.get("case_id") or "custom", "customer_id": ctx.get("customer_id") or customer.get("id"),
                "message": ctx.get("message") or "", "history": ctx.get("history") or []}
        if not case["customer_id"]:
            return _result(error="C3 needs a customer id, and this email has none.")
        started = time.time()
        try:
            runner = self._load()
            if self._native:
                from lab.acme import use_data_root
                from lab.version_c3 import build_decision_envelope
                with use_data_root(self.data_root or self.lab_root / "data" / "acme"):
                    envelope = build_decision_envelope(case)
                    output, turns = runner(case, temperature=self.temperature, run=ctx.get("sample", 0),
                                           model=self.model, max_steps=self.max_steps, envelope=envelope,
                                           timeout=self.timeout, persist_cache=self.persist_cache)
                row = {**output, "envelope": envelope, "turns": turns, "steps": len(turns),
                       "tool_calls": [{"step": turn["step"], "name": call[0], "args": call[1], "result": call[2]}
                                      for turn in turns for call in turn["tool_calls"]],
                       "tokens_in": sum(turn["tokens_in"] for turn in turns),
                       "tokens_out": sum(turn["tokens_out"] for turn in turns)}
            else:
                row = runner(case)
        except Exception as exc:  # noqa: BLE001 - an API limit or a lab error becomes a model error in step 5
            return _result(error=f"C3 failed: {exc}"[:400], latency=time.time() - started)
        return _result(output=c3_output(row, ctx.get("outage")), latency=time.time() - started,
                       raw=json.dumps(row, ensure_ascii=False, default=str))


def make_provider(name: str, model: str = "sonnet"):
    if name == "claude-code":
        return ClaudeCodeProvider(model=model)
    if name == "c3":
        return C3Provider()
    return OfflineProvider()
