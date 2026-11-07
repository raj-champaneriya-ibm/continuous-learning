"""Deterministic business rules engine, decoupled from the OWL ontology (data/acme/business_rules.json).

Why separate from ontology.ttl?
- The ontology (TBox) defines *meaning* and *relationships*: what a 'concession', 'late-fee waiver',
  'retention offer', 'account holder' or 'broadband plan' is, and which concepts count toward limits.
- Business rules define *operational thresholds and commercial policy*: ₹500 vs ₹750 limit, 13-month
  tenure gate, 12-month cooldown window, 50% retention discount. Commercial teams change these parameters
  without altering the ontological hierarchy or agent code.
"""
from __future__ import annotations

import copy
import json
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from .acme import DATA, RECORD_DATE

RULES_FILE = DATA / "business_rules.json"


@lru_cache(maxsize=1)
def _default_rules() -> Dict[str, Any]:
    return json.loads(RULES_FILE.read_text(encoding="utf-8"))


def load_business_rules(path: Optional[Path] = None,
                        overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Load the declarative business rule set, optionally applying commercial overrides."""
    base = json.loads(path.read_text(encoding="utf-8")) if path else copy.deepcopy(_default_rules())
    if overrides:
        _deep_update(base, overrides)
    return base


def _deep_update(target: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_update(target[key], value)
        else:
            target[key] = copy.deepcopy(value)
    return target


def _parse_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    return datetime.strptime(str(value).strip()[:10], "%Y-%m-%d").date()


def months_since(used_on: Optional[str], as_of: str = RECORD_DATE) -> Optional[int]:
    """Whole calendar months elapsed between `used_on` and `as_of` (e.g. '2026-10-25')."""
    used = _parse_date(used_on)
    ref = _parse_date(as_of)
    if used is None or ref is None:
        return None
    months = (ref.year - used.year) * 12 + (ref.month - used.month)
    if ref.day < used.day:
        months -= 1
    return months


def duplicate_payment_amount(payments: List[int]) -> Optional[int]:
    """Return the duplicated payment amount if the cycle record shows the same payment twice."""
    seen = set()
    for p in payments or []:
        if p in seen:
            return int(p)
        seen.add(p)
    return None


def outage_exceeds_hours(outage: Optional[Dict[str, Any]], min_hours: int = 24) -> bool:
    """Does the active outage record explicitly indicate it has lasted more than `min_hours`?"""
    if not outage:
        return False
    since = str(outage.get("since") or "").lower()
    if "days" in since or "48 hours" in since or "more than 24" in since:
        return True
    # "today 06:40" and "yesterday 22:10" (as of morning on 2026-10-25) are both under 24 hours.
    return False
