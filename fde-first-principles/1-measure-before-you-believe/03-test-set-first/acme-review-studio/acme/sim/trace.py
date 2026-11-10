"""The common input, output and trace contract for simulator adapters."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Protocol

ImplementationModel = Literal["orchestrated", "declarative", "agent_loop", "multi_agent", "api", "custom"]
SpanKind = Literal["step", "model_call", "tool_call", "agent", "handoff", "guard", "check", "human", "http"]
RunState = Literal["queued", "running", "completed", "waiting_for_human", "failed", "abandoned"]
SPAN_KINDS = frozenset({"step", "model_call", "tool_call", "agent", "handoff", "guard", "check", "human", "http"})
SPAN_STATUSES = frozenset({"ok", "flag", "stop", "error", "escalate", "waiting", "skipped"})


@dataclass(frozen=True)
class Capabilities:
    interrupt: bool = False
    prompts: bool = False
    tool_calls: bool = False
    envelope: bool = False
    recorded_replay: bool = False
    remote_trace: bool = False


@dataclass(frozen=True)
class Span:
    id: str
    parent: str | None
    kind: SpanKind
    name: str
    status: str
    ms: int
    attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.kind not in SPAN_KINDS or self.status not in SPAN_STATUSES:
            raise ValueError(f"Unknown span kind or status: {self.kind!r}, {self.status!r}")
        if not self.id or self.ms < 0:
            raise ValueError("A span needs an id and a non-negative duration")


@dataclass(frozen=True)
class Topology:
    nodes: list[dict[str, Any]] = field(default_factory=list)
    edges: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class RunInput:
    customer_id: str
    message: str
    case_id: str = "custom"
    portal: str = "email"
    history: list[dict[str, str]] = field(default_factory=list)
    case: dict[str, Any] | None = None

    @classmethod
    def from_case(cls, case: dict[str, Any], portal: str = "email") -> RunInput:
        return cls(customer_id=case["customer_id"], message=case["message"], case_id=case["id"],
                   portal=portal, history=list(case.get("history") or []), case=dict(case))


@dataclass
class RunResult:
    run_id: str
    version_id: str
    state: RunState
    output: dict[str, Any] | None = None
    spans: list[Span] = field(default_factory=list)
    usage: dict[str, Any] = field(default_factory=dict)
    pins: dict[str, Any] = field(default_factory=dict)
    case_hash: str = ""
    label_hash: str = ""
    grade: dict[str, Any] = field(default_factory=dict)
    drift: list[str] = field(default_factory=list)
    sample: int = 0
    batch_id: str | None = None
    replay_of: str | None = None
    audit: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RunResult:
        return cls(**{**data, "spans": [Span(**s) for s in data.get("spans", [])]})


class Adapter(Protocol):
    implementation: ImplementationModel

    def capabilities(self, version: Any) -> Capabilities: ...
    def status(self, version: Any) -> tuple[bool, str]: ...
    def input_schema(self, version: Any) -> dict[str, Any]: ...
    def topology(self, version: Any) -> Topology: ...
    def start(self, version: Any, run_input: RunInput, run_id: str, sample: int = 0,
              recorded: dict[str, Any] | None = None) -> RunResult: ...
    def resume(self, version: Any, run_id: str, decision: dict[str, Any]) -> RunResult: ...
