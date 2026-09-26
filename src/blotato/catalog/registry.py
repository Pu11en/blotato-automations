"""Auto-discovers every template module under catalog/templates/ and
exposes them as one registry, keyed by our catalog id (not Blotato's
templateId, which can be a long UUID or path -- our ids are short and
stable even if Blotato reshuffles internal ids).

A module contributes either a single `ENTRY` or an `ENTRIES` iterable, so a
family of templates that differ only by id and label (Blotato ships 20
infographic styles with identical inputs) stays one file instead of 20
near-identical ones."""
from __future__ import annotations

import importlib
import pkgutil
from typing import Iterator

from . import templates as _templates_pkg
from .types import ModelEntry


class UnknownModelError(KeyError):
    pass


def _discover() -> dict:
    registry = {}
    for module_info in pkgutil.iter_modules(_templates_pkg.__path__):
        module = importlib.import_module(f"{_templates_pkg.__name__}.{module_info.name}")
        entries = getattr(module, "ENTRIES", None)
        if entries is None:
            single = getattr(module, "ENTRY", None)
            entries = () if single is None else (single,)
        for entry in entries:
            if not isinstance(entry, ModelEntry):
                raise TypeError(f"{module.__name__} exported a non-ModelEntry: {entry!r}")
            if entry.id in registry:
                raise ValueError(f"duplicate catalog id: {entry.id}")
            registry[entry.id] = entry
    return registry


_REGISTRY = None


def _registry() -> dict:
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _discover()
    return _REGISTRY


def get_model(model_id: str) -> ModelEntry:
    try:
        return _registry()[model_id]
    except KeyError:
        raise UnknownModelError(model_id) from None


def list_models(*, surface: str = None, include_broken: bool = True) -> list:
    entries = list(_registry().values())
    if surface is not None:
        entries = [e for e in entries if e.surface == surface]
    if not include_broken:
        entries = [e for e in entries if not e.is_known_broken]
    return sorted(entries, key=lambda e: e.id)
