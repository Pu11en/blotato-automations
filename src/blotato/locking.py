"""Cross-platform exclusive directory lock.

The Pinterest workflow used ``fcntl.flock`` directly. ``fcntl`` does not
exist on Windows, so importing it took the entire workflow -- and three
test modules -- down on any Windows machine. This keeps the blocking-lock
semantics and adds an explicit timeout instead of waiting forever.
"""
from __future__ import annotations

import contextlib
import time
from pathlib import Path

try:  # POSIX
    import fcntl

    msvcrt = None
except ImportError:  # Windows
    fcntl = None
    import msvcrt


class LockTimeout(RuntimeError):
    pass


def _try_acquire(handle) -> bool:
    if fcntl is not None:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            return False
    handle.seek(0)
    try:
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        return True
    except OSError:
        return False


def _release(handle) -> None:
    if fcntl is not None:
        fcntl.flock(handle, fcntl.LOCK_UN)
        return
    handle.seek(0)
    with contextlib.suppress(OSError):
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


@contextlib.contextmanager
def exclusive_lock(directory, *, timeout: float = 30.0, poll: float = 0.05):
    """Hold an exclusive lock on `directory`/.lock for the block's duration."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".lock").open("a+") as handle:
        deadline = time.monotonic() + timeout
        while not _try_acquire(handle):
            if time.monotonic() >= deadline:
                raise LockTimeout(f"could not lock {directory} within {timeout}s")
            time.sleep(poll)
        try:
            yield directory
        finally:
            _release(handle)
