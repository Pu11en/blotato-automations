"""The technique registry, keyed by our own catalog id.

Ids are ours, not Blotato's `templateId` -- theirs are long UUIDs or paths
and can be reshuffled; ours are short and stable.

Entries come from three places, in this order:

1. **Built-in modules** under `catalog/templates/`. A module contributes a
   single `ENTRY` or an `ENTRIES` iterable, so a family of templates that
   differ only by id and label stays one file.
2. **Other installed packages**, via the `blotato.techniques` entry point.
   This is how a consuming project (youtube-money, a client repo) adds its
   own techniques without forking this one -- see
   `docs/using-from-another-project.md`.
3. **Runtime registration** with `register()`, for a project that would
   rather not declare an entry point.

A duplicate id is an error rather than a silent override: two packages
disagreeing about what `video.story` means is a bug worth surfacing loudly,
not resolving by import order.
"""
from __future__ import annotations

import importlib
import pkgutil
from typing import Iterable

from . import templates as _templates_pkg
from .types import ModelEntry

ENTRY_POINT_GROUP = "blotato.techniques"


class UnknownModelError(KeyError):
    pass


class DuplicateModelError(ValueError):
    pass


_EXTRA: dict = {}
_REGISTRY = None


def _entries_from(source, label: str) -> Iterable[ModelEntry]:
    entries = getattr(source, "ENTRIES", None)
    if entries is None:
        single = getattr(source, "ENTRY", None)
        entries = () if single is None else (single,)
    for entry in entries:
        if not isinstance(entry, ModelEntry):
            raise TypeError(f"{label} exported a non-ModelEntry: {entry!r}")
        yield entry


def _add(registry: dict, entry: ModelEntry, origin: str) -> None:
    existing = registry.get(entry.id)
    if existing is not None:
        raise DuplicateModelError(
            f"two techniques claim the id {entry.id!r}: {existing.origin} and {origin}"
        )
    registry[entry.id] = entry.with_origin(origin)


def _discover_builtin(registry: dict) -> None:
    for module_info in pkgutil.iter_modules(_templates_pkg.__path__):
        name = f"{_templates_pkg.__name__}.{module_info.name}"
        module = importlib.import_module(name)
        for entry in _entries_from(module, name):
            _add(registry, entry, "blotato")


def _discover_plugins(registry: dict) -> None:
    """Load techniques contributed by any other installed package."""
    from importlib.metadata import entry_points

    for point in entry_points(group=ENTRY_POINT_GROUP):
        try:
            loaded = point.load()
        except Exception as exc:  # a broken plugin must not take the CLI down
            raise RuntimeError(
                f"technique plugin {point.value!r} (from {point.name!r}) failed to import: {exc}"
            ) from exc
        for entry in _entries_from(loaded, point.value):
            _add(registry, entry, point.name)


def _discover() -> dict:
    registry: dict = {}
    _discover_builtin(registry)
    _discover_plugins(registry)
    for entry, origin in _EXTRA.values():
        _add(registry, entry, origin)
    return registry


def _registry() -> dict:
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _discover()
    return _REGISTRY


def register(entry: ModelEntry, *, origin: str = "runtime") -> None:
    """Add a technique from a consuming project at runtime.

    Prefer the `blotato.techniques` entry point, which makes the technique
    visible to the `blotato` CLI too. Use this when the entries are built
    dynamically, or in a test.
    """
    if not isinstance(entry, ModelEntry):
        raise TypeError(f"expected a ModelEntry, got {entry!r}")
    _EXTRA[entry.id] = (entry, origin)
    reset()


def reset() -> None:
    """Drop the cached registry so the next lookup rediscovers everything."""
    global _REGISTRY
    _REGISTRY = None


def get_model(model_id: str) -> ModelEntry:
    try:
        return _registry()[model_id]
    except KeyError:
        raise UnknownModelError(model_id) from None


def list_models(
    *,
    surface: str = None,
    include_broken: bool = True,
    origin: str = None,
) -> list:
    entries = list(_registry().values())
    if surface is not None:
        entries = [e for e in entries if e.surface == surface]
    if not include_broken:
        entries = [e for e in entries if not e.is_known_broken]
    if origin is not None:
        entries = [e for e in entries if e.origin == origin]
    return sorted(entries, key=lambda e: e.id)


def origins() -> list:
    """Every package currently contributing techniques."""
    return sorted({e.origin for e in _registry().values()})
