"""Review-page rules: which failure mode to preselect, and when a verdict may be saved."""
from __future__ import annotations

from .checks import eval_checks


def suggest_mode(case: dict, rec: dict) -> str:
    ev = eval_checks(case, rec)
    flags = {f["check"] for f in rec.get("flags", [])}
    if ev["routing_ok"] is False and case["needs_human"]:
        return "Missed escalation"                      # the costliest failure comes first
    for flag, mode in [("time promise", "Promised fix time"), ("financial promise", "Financial promise > ₹500"),
                       ("other customer's data", "Privacy leak"), ("asks for a secret", "Asked for a secret"),
                       ("unsupported ticket", "Unsupported claim"), ("unsupported amount", "Unsupported claim")]:
        if flag in flags:
            return mode
    if ev["banned"]:
        return "Unsupported claim"
    if ev["missing"]:
        return "Missing required fact"
    if ev["routing_ok"] is False:
        return "Unneeded escalation"
    if ev["intent_ok"] is False:
        return "Wrong intent"
    return ""


def initial_mode(case: dict, rec: dict, critique_first: bool) -> str:
    """Mode preselected when a case opens: none in critique-first review, else the suggestion."""
    if critique_first or rec.get("verdict") or not (rec.get("reply") or rec.get("decision")):
        return ""
    return suggest_mode(case, rec)


def validate_verdict(verdict: str, mode: str, critique: str, critique_first: bool) -> str:
    """'' when the verdict may be saved, else what the expert still has to give."""
    if verdict == "Fail":
        if not critique:
            return "write a short critique"
        if not mode and not critique_first:
            return "pick a failure mode"
    return ""
