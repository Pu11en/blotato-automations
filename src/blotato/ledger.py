"""An append-only record of every paid call, and an optional cap on a run.

`max_credits_ceiling` bounds one call. Nothing bounded the *sum*: a script
looping over `submit` with a 60-credit ceiling could spend the whole balance,
60 at a time, and every individual call would look correct. This adds the
missing layer -- a named run with a cumulative budget -- ported from the
ledger the youtube-money repo grew for the same reason.

The ledger lives at `<workspace>/outputs/credits.log`, one JSON object per
line, appended and never rewritten. It is a record, not a cache: the live
balance from the API is always the final word, and the ledger only answers
"how much has *this run* spent so far".
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Optional

from .locking import exclusive_lock
from .workspace import workspace_root

LEDGER_NAME = "credits.log"


class BudgetExceeded(RuntimeError):
    pass


def ledger_path(*, workspace: Optional[Path] = None) -> Path:
    return workspace_root(workspace) / "outputs" / LEDGER_NAME


def record(
    entry: dict,
    *,
    workspace: Optional[Path] = None,
) -> Path:
    """Append one spend record. Never raises on a malformed existing file."""
    path = ledger_path(workspace=workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **entry}
    # Two processes appending at once must not interleave a half-written line.
    with exclusive_lock(path.parent):
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
    return path


def entries(*, run: Optional[str] = None, workspace: Optional[Path] = None) -> list:
    path = ledger_path(workspace=workspace)
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            # A truncated line from a killed process must not hide the rest.
            continue
        if run is None or row.get("run") == run:
            rows.append(row)
    return rows


def spent(*, run: Optional[str] = None, workspace: Optional[Path] = None) -> float:
    """Credits this run has already spent.

    A call whose delta could not be measured counts as its full ceiling
    rather than as zero -- guessing low is how a budget gets blown.
    """
    total = 0.0
    for row in entries(run=run, workspace=workspace):
        delta = row.get("credits_observed_delta")
        if delta is None:
            delta = row.get("assumed_credits") or 0
        total += float(delta)
    return total


def check_budget(
    *,
    run: Optional[str],
    budget: Optional[float],
    ceiling: float,
    workspace: Optional[Path] = None,
) -> float:
    """Raise unless this call still fits inside the run's budget.

    Returns what the run has spent so far. A budget with no run name is a
    mistake worth catching: there would be nothing to accumulate against.
    """
    if budget is None:
        return spent(run=run, workspace=workspace) if run else 0.0
    if not run:
        raise ValueError("a budget needs a run name to accumulate against")
    if budget <= 0:
        raise ValueError("budget must be positive")
    already = spent(run=run, workspace=workspace)
    if already + ceiling > budget:
        raise BudgetExceeded(
            f"run {run!r} has spent {already:g} of its {budget:g}-credit budget; "
            f"this call could spend {ceiling:g} more, which would exceed it"
        )
    return already
